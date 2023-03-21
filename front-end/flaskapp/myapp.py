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
ip_addr = '10.0.0.218'
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signout/')
def signout():
    session.pop('user_data', None)
    return render_template('signout.html')
# ...
@app.route('/authenticated_index/')
def authenticated_index():
    if 'user_data' in session:
        return render_template('authenticated_index.html', user_data=session['user_data'])
    else:
        return redirect(url_for('index'))

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
        front_end_sign_in = Send.send(ip_addr,port,username,password,vhost,exchange,signin_queue,signin_routing_key,exchange_type)
        json_user_data = json.dumps(user_sign_in)
        front_end_sign_in.send_message(json_user_data)

        flash('Invalid email or password')

        receive_sign_in = Receive.recieve(ip_addr,port,username,password,vhost,fe_userexist_queue,fe_userexist_routing_key,receive_from_exchange, exchange_type)
        json_response = {}
        receive_sign_in.receive_message(json_response)

        if json_response:
            print(type(json_response))
            user_data = json.dumps(json_response)
            print(user_data)
            if user_data:
                session['user_data'] = json.loads(user_data)
                return redirect(url_for('authenticated_index'))

    return render_template('signin.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Retrieve the form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        passwd = request.form['password']
        address = request.form['address']
        zip = request.form['zip']
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
            'receive_emails': email_toggle
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

    return render_template('register.html')


if __name__ == '__main__':
	app.run(host='localhost', port=7007)

