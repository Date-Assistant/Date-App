from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
import pika
import sys
import json
import Receive
import Send
import os
import tempfile

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback secret key')  # Use fallback secret key if not found in environment variables
Session(app)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

username = 'brian'
password = 'password'
ip_addr = '10.0.0.209'
port = 5672
vhost = 'cherry_broker'
registration_queue= 'registration'
signin_queue = 'signin'

exchange = 'fe2be'
exchange_type = 'direct'

register_routing_key = 'registration'
signin_routing_key = 'signin'


fe_userexist_queue = 'existinguser'
fe_userexist_routing_key = 'existinguser'
receive_from_exchange = 'be2fe'

fe_usernoexist_queue = 'nonexistinguser'
fe_usernoexist_routing_key = 'nonexistinguser'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signout/')
def signout():
    session.pop('user_data', None)
    return render_template('signout.html')

@app.route('/claim_offer_unauthenticated', methods=['POST'])
def claim_offer_unauthenticated():
    offer_reply = request.form.get('offer_reply', 'false')
    discount_code = 'DATEAPP15'
    if offer_reply == 'true':
        session['discount_code'] = discount_code
        return redirect(url_for('register'))
    else:
        session.pop('discount_code', None)
        return redirect(url_for('index'))

@app.route('/claim_offer', methods=['POST'])
def claim_offer():
    offer_reply = request.form.get('offer_reply', 'false')
    # TODO: Process the user's response and store it in the database
    return {'status': 'success'}

# ...
@app.route('/authenticated_index/')
def authenticated_index():
    if 'user_data' in session:
        return render_template('authenticated_index.html', user_data=session['user_data'])
    else:
        return redirect(url_for('index'))
    
@app.route('/pricing', methods=['GET'])
def pricing():
    if 'user_data' in session:
        fname = session['user_data']['first_name']
        return render_template('pricing.html', fname=fname)
    else:
        return redirect(url_for('login'))
    
@app.route('/non_user_pricing', methods=['GET'])
def non_user_pricing():
    return render_template('non_pricing.html', fname='Dater!')

@app.route('/non_user_pricing_submit', methods=['POST'])
def non_user_pricing_submit():
    if 'user_data' not in session:
        flash("You must register first")
        return redirect(url_for('register'))
    plan = request.form['plan']
    cardholder_name = request.form['cardholderName']
    card_number = request.form['cardNumber']
    expiration_month = request.form.get('expiration-month')
    expiration_year = request.form.get('expiration-year')
    cvc = request.form.get('cvc')
    save_card_info = request.form.get('saveCardInfo', 'no')

    expiration_date = f"{expiration_month}/{expiration_year}"

    # Perform validation, e.g., check the length of the credit card number
    if len(card_number) != 16:
        # Return an error or redirect to an error page
        return "Invalid card number"

    payment_info = {
        'plan': plan,
        'cardholder_name': cardholder_name,
        'card_number': card_number,
        'expiration_date': expiration_date,
        'cvc': cvc,
        'saveCardInfo': save_card_info
    }
    print(payment_info)

    # Redirect to postregister.html if the information is valid
    return redirect(url_for('postregister'))


@app.route('/pricing_submit', methods=['POST'])
def pricing_submit():
    plan = request.form['plan']
    cardholder_name = request.form['cardholderName']
    card_number = request.form['cardNumber']
    expiration_month = request.form.get('expiration-month')
    expiration_year = request.form.get('expiration-year')
    cvc = request.form.get('cvc')
    save_card_info = request.form.get('saveCardInfo', 'no')

    expiration_date = f"{expiration_month}/{expiration_year}"

    # Perform validation, e.g., check the length of the credit card number
    if len(card_number) != 16:
        # Return an error or redirect to an error page
        return "Invalid card number"

    payment_info = {
        'plan': plan,
        'cardholder_name': cardholder_name,
        'card_number': card_number,
        'expiration_date': expiration_date,
        'cvc': cvc,
        'saveCardInfo': save_card_info
    }
    print(payment_info)

    # Redirect to postregister.html if the information is valid
    return redirect(url_for('postregister'))


@app.route('/signin/', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        # Retrieve the form data
        email = request.form['email']
        passwd = request.form['password']

        # Create a dictionary to store the form data
        user_sign_in = {
            'email': email,
            'password' : passwd,
        }

        # Print the form data
        front_end_sign_in = Send.Send(ip_addr,port,username,password,vhost,exchange,signin_queue,exchange_type)
        json_user_data = json.dumps(user_sign_in)
        front_end_sign_in.send_message(json_user_data,signin_routing_key)

        flash('Invalid email or password')

        
        receive_sign_in = Receive.recieve(ip_addr,port,username,password,vhost,fe_userexist_queue,fe_userexist_routing_key,receive_from_exchange, exchange_type)
        json_response = {}

        while True:
            result = receive_sign_in.receive_message(json_response)
            if result:
                print(json_response)
                break


        if json_response:
            user_data = json.dumps(json_response)
            if('error' in user_data):
                return redirect(url_for('index'))
            else:
                session['user_data'] = json.loads(user_data)
                return redirect(url_for('authenticated_index'))

    return render_template('signin.html')

'''
    if json_response:
        user_data = json.dumps(json_response)
        print(user_data)
        tempDict = {}
        for x in user_data:
            if(x == 'first_name'):
                tempDict = {x:user_data[x]}
            if(x == 'last_name'):
                tempDict = {x:user_data[x]}
            if(x == 'email'):
                tempDict = {x:user_data[x]}
            if(x == 'password'):
                tempDict = {x:user_data[x]}
            else:
                if(x == 'error'):
                    print('error')
                    return redirect(url_for('index'))
        user_data_final = json.dumps(tempDict)
        session['user_data'] = json.loads(user_data_final)
        receive_sign_in.close()
        return redirect(url_for('authenticated_index'))
'''


@app.route('/register/', methods=('GET', 'POST'))
def register():
    basic_price = 5.99
    premium_price = 19.99
    discount_percentage = 0.85
    if request.method == 'POST':
        # Retrieve the form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        passwd = request.form['password']
        address = request.form['address']
        zip = request.form['zip']
        discountCode = request.form['discountCode']
        email_toggle = request.form.get('email-toggle', 'off')

        # Create a dictionary to store the form data
        user_data = {
            'first_name': fname,
            'last_name': lname,
            'email': email,
            'password' : passwd,
            'phone': phone,
            'address': address,
            'zip_code': zip,
            'receive_emails': email_toggle,
            'discountCode' : discountCode
        }

        # Print the form data
        try:
            front_end_register = Send.send(ip_addr,port,username,password,vhost,exchange,registration_queue,register_routing_key,exchange_type)
            json_user_data = json.dumps(user_data)
            front_end_register.send_message(json_user_data)
            return render_template('postregister.html')
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

    return render_template('register.html', basic_price=basic_price, premium_price=premium_price, discount_percentage=discount_percentage)

@app.route('/register2/', methods=('GET', 'POST'))
def register2():
    basic_price = 39.99
    premium_price = 79.99
    discount_percentage = 0.85
    if request.method == 'POST':
        # Retrieve the form data
        bname = request.form['bname']
        oname = request.form['oname']
        email = request.form['email']
        phone = request.form['phone']
        passwd = request.form['password']
        address = request.form['address']
        zip = request.form['zip']
        discountCode = request.form['discountCode']
        email_toggle = request.form.get('email-toggle', 'off')

        # Create a dictionary to store the form data
        user_data = {
            'business_name': bname,
            'owner_name': oname,
            'email': email,
            'password' : passwd,
            'phone': phone,
            'address': address,
            'zip_code': zip,
            'receive_emails': email_toggle,
            'discountCode' : discountCode
        }

        # Print the form data
        try:
            front_end_register = Send.send(ip_addr,port,username,password,vhost,exchange,registration_queue,register_routing_key,exchange_type)
            json_user_data = json.dumps(user_data)
            front_end_register.send_message(json_user_data)
            return render_template('postregister.html')
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

    return render_template('register2.html', basic_price=basic_price, premium_price=premium_price, discount_percentage=discount_percentage)




if __name__ == '__main__':
	app.run(host='localhost', port=7007)

