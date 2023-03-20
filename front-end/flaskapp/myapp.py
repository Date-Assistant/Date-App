from flask import Flask, render_template, request, url_for, flash, redirect
import pika
import sys
import json
import Receive
import Send

app = Flask(__name__)

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
queue= 'queue1'
signin_queue = 'testqueue'
exchange = 'fe2be'
exchange_type = 'direct'
register_routing_key = 'queue1'
signin_routing_key = 'signin'

@app.route('/')
def index():
    return render_template('index.html')

# ...

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
        try:
            front_end_sign_in = Send.send(ip_addr,port,username,password,vhost,exchange,signin_queue,signin_routing_key,exchange_type)
            json_user_data = json.dumps(user_sign_in)
            front_end_sign_in.send_message(json_user_data)
            return redirect(url_for('index'))
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

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
            front_end_register = Send.send(ip_addr,port,username,password,vhost,exchange,queue,register_routing_key,exchange_type)
            json_user_data = json.dumps(user_data)
            front_end_register.send_message(json_user_data)
            return redirect(url_for('signin'))
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

    return render_template('register.html')


if __name__ == '__main__':
	app.run(host='localhost', port=7007)

