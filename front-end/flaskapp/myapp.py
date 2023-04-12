from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import os
import tempfile
import time
import requests


app = Flask(__name__)
#yelp_api_key 
#api_key = open('API_KEY.txt').read() 
api_key = 'C6oVTJvz932BtQjLQroxFp_dgk4gRkVJMD0Tthr0ThYI7W1RDuFR5p2I2ipKnBWvkvjF4LEehQZ-Fh5DcdRDCJvEPlx8A6h4OZY8eAO4Q5DvlYcl2GkT93ZYGXsTZHYx'

"""
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback secret key')  # Use fallback secret key if not found in environment variables
Session(app)
"""

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

        rabbitmq = RabbitMQClient(
            host='18.234.152.143', 
            username='it490admin', 
            password='password'
        )
        rabbitmq.connect()
        rabbitmq.declare_queue("signin")
        son_user_data = json.dumps(user_sign_in)
        rabbitmq.send_message(exchange="", routing_key="signin", body=son_user_data)
        rabbitmq.close()

        print("waiting for response")
        rabbitmq.connect()

        while True:
            result = rabbitmq.consume_messages("redirectlogin")
            if result:
                rabbitmq.close()
                print(result)
                break
            else:
                print('connection does not work')
            time.sleep(1)

        for key in result:
            if key == "Yes":
                session['user_data'] = result
                return redirect(url_for('authenticated_index'))
            if key == "No":
                return redirect(url_for('register2'))
        
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
            rabbitmq = RabbitMQClient(
                host='18.234.152.143', 
                username='it490admin', 
                password='password'
            )
            rabbitmq.connect()
            rabbitmq.declare_queue("register")
            json_user_data = json.dumps(user_data)
            rabbitmq.send_message(exchange="", routing_key="register", body=json_user_data)
            rabbitmq.close()  
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
            rabbitmq = send(
                    "b-6a393830-73ed-476c-9530-c0b5029109d0",
                    "it490admin",
                    "c7dvcdbtgpue",
                    "us-east-1"
                )
            rabbitmq.declare_queue("register2")
            json_user_data = json.dumps(user_data)
            rabbitmq.send_message(exchange="", routing_key="register2", body=json_user_data)
            rabbitmq.close()  
            return render_template('postregister.html')
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

    return render_template('register2.html', basic_price=basic_price, premium_price=premium_price, discount_percentage=discount_percentage)


@app.route('/search_restaurants')
def search_restaurants():
    return render_template('search_restaurants.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    API_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    if request.method == 'POST':
        location = request.form.get('location')
        term = request.form.get('term')

        # Set the parameters for the Yelp API request
        params = {
            'location': location,
            'term': term,
            'sort_by': 'rating',
            'limit': 10
        }

        # Set the headers for the API request
        headers = {
            'Authorization': 'Bearer %s' % api_key
        }

        # Make the API request
        response = requests.get(API_ENDPOINT, params=params, headers=headers)
        businesses = response.json().get('businesses')

        # Render the HTML template with the list of businesses
        return render_template('search.html', businesses=businesses)

    return render_template('index.html')

@app.route('/business/<id>')
def business_details(id):
    # Set the headers for the API request
    print("ID=" + id )
    headers = {
        'Authorization': 'Bearer %s' % api_key
    }

    # Make the API request to retrieve details for the specified business ID
    response = requests.get(f'https://api.yelp.com/v3/businesses/{id}', headers=headers)
    business = response.json()
    print(response)

    # Render the HTML template with the business details
    return render_template('details.html', business=business)


if __name__ == '__main__':
	app.run(host='localhost', port=7007)

