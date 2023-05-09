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
import threading
from yelpapi import YelpAPI


app = Flask(__name__)
#yelp_api_key 
#api_key = open('API_KEY.txt').read() 
api_key = 'C6oVTJvz932BtQjLQroxFp_dgk4gRkVJMD0Tthr0ThYI7W1RDuFR5p2I2ipKnBWvkvjF4LEehQZ-Fh5DcdRDCJvEPlx8A6h4OZY8eAO4Q5DvlYcl2GkT93ZYGXsTZHYx'
YELP_API_KEY = "C6oVTJvz932BtQjLQroxFp_dgk4gRkVJMD0Tthr0ThYI7W1RDuFR5p2I2ipKnBWvkvjF4LEehQZ-Fh5DcdRDCJvEPlx8A6h4OZY8eAO4Q5DvlYcl2GkT93ZYGXsTZHYx"
WEATHER_API_KEY = "5d4ff4f2e99e0cce15a54a4f247fcc58"
yelp_api = YelpAPI(YELP_API_KEY)


app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback secret key')  # Use fallback secret key if not found in environment variables
Session(app)


#helper functions
def get_weather_data(location, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def get_yelp_data(location, term, preferences):
    activity_mapping = {
        'food': 'restaurants',
        'outdoors': 'outdoor, hiking, park, trails',
        'arts': 'arts, museums, galleries',
        'entertainment': 'entertainment, movies, theater'
    }
    activity_term = activity_mapping.get(term, term)
    if term == 'food' and preferences != 'any':
        activity_term = f"{activity_term}, {preferences}"

    response = yelp_api.search_query(term=activity_term, location=location, sort_by='best_match', limit=10)
    return response.get('businesses', [])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signout/')
def signout():
    session.pop('user_data', None)
    return render_template('signout.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

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
        plan = session.get('plan')  # Get the plan from the session
        return render_template('pricing.html', fname=fname, plan=plan)
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


@app.route('/postchangepassword', methods=['GET'])
def postchangepassword():
    return render_template('postchangepassword.html')


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

    session.pop('plan', None)  # Remove the plan from the session
    return redirect(url_for('authenticated_index'))


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
            username='it490admin', 
            password='password'
        )
        rabbitmq.connect()
        rabbitmq.declare_queue("signin")
        son_user_data = json.dumps(user_sign_in)
        rabbitmq.send_message(exchange="", routing_key="signin", body=son_user_data)
        rabbitmq.close()

        received_event = threading.Event() # to signal when the message is received
        message_container = [None] # to store the received message

        rabbitmq.connect()
        print("waiting for response")
        rabbitmq.consume_messages("redirectlogin", received_event, message_container)
        received_event.wait() # wait for the message to be received
        result = message_container[0] # get the received message
        rabbitmq.close()

        for key in result:
            if key == "Yes":
                session['user_data'] = result
                return redirect(url_for('authenticated_index'))
            if key == "No":
                return redirect(url_for('register2'))
        
    return render_template('signin.html')

@app.route('/business_signin/', methods=('GET', 'POST'))
def business_signin():
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
            username='it490admin', 
            password='password'
        )
        rabbitmq.connect()
        rabbitmq.declare_queue("signin")
        son_user_data = json.dumps(user_sign_in)
        rabbitmq.send_message(exchange="", routing_key="signin", body=son_user_data)
        rabbitmq.close()

        received_event = threading.Event() # to signal when the message is received
        message_container = [None] # to store the received message

        rabbitmq.connect()
        print("waiting for response")
        rabbitmq.consume_messages("redirectlogin", received_event, message_container)
        received_event.wait() # wait for the message to be received
        result = message_container[0] # get the received message
        rabbitmq.close()

        for key in result:
            if key == "Yes":
                session['user_data'] = result
                return redirect(url_for('authenticated_index'))
            if key == "No":
                return redirect(url_for('register2'))
        
    return render_template('signin.html')


@app.route('/register/', methods=('GET', 'POST'))
def register():
    plan = request.args.get('plan')
    if plan:
        session['plan'] = plan
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
        confirm_passwd = request.form['confirmPassword']
        address = request.form['address']
        zip = request.form['zip']
        discountCode = request.form['discountCode']
        email_toggle = request.form.get('email-toggle', 'off')
        membership_type = request.form['membership_type']

        if passwd != confirm_passwd:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

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
            'discountCode' : discountCode,
            'membership_type' : membership_type
        }

        # Print the form data
        try:
            rabbitmq = RabbitMQClient(
                username='it490admin', 
                password='password'
            )
            rabbitmq.connect()
            rabbitmq.declare_queue("register")
            json_user_data = json.dumps(user_data)
            rabbitmq.send_message(exchange="", routing_key="register", body=json_user_data)
            rabbitmq.close()  
            session['user_data'] = user_data
    
            # Redirect to pricing page
            return redirect(url_for('pricing'))
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

    return render_template('register.html', basic_price=basic_price, premium_price=premium_price, discount_percentage=discount_percentage)

@app.route('/register2/', methods=('GET', 'POST'))
def register2():
    basic_price = 39.99
    premium_price = 79.99
    discount_percentage = 0.85
    plan = request.args.get('plan')
    if plan:
        session['plan'] = plan
    if request.method == 'POST':
        # Retrieve the form data
        bname = request.form['bname']
        oname = request.form['oname']
        email = request.form['email']
        phone = request.form['phone']
        passwd = request.form['password']
        confirm_passwd = request.form['confirmPassword']
        address = request.form['address']
        zip = request.form['zip']
        discountCode = request.form['discountCode']
        email_toggle = request.form.get('email-toggle', 'off')
        membership_type = request.form['membership_type']

        # Check if the passwords match
        if passwd != confirm_passwd:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register2'))

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
            'discountCode' : discountCode,
            'membership_type' : membership_type
        }

        # Print the form data
        try:
            rabbitmq = RabbitMQClient(
                    "it490admin",
                    "c7dvcdbtgpue",
                )
            rabbitmq.connect()
            rabbitmq.declare_queue("register2")
            json_user_data = json.dumps(user_data)
            rabbitmq.send_message(exchange="", routing_key="register2", body=json_user_data)
            rabbitmq.close()  
            session['user_data'] = user_data
    
            # Redirect to pricing page
            return redirect(url_for('pricing'))
        except BaseException:
            print("error")

        # TODO: Add code to store the data in a database or message queue

    return render_template('register2.html', basic_price=basic_price, premium_price=premium_price, discount_percentage=discount_percentage)


@app.route('/search_restaurants')
def search_restaurants():
    return render_template('search_restaurants.html')

@app.route('/activity_recommender')
def activity_recommender():
    return render_template('activity_recommender.html')

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

@app.route('/saved_idea/<id>')
def saved_idea(id):
    print("ID=" + id )
    #data = {"ID": id , "Email" : session['user_data']['email']}
    data = {
        'id': id,
        'email' : "ll452@njit.edu",
        }
    print(data)

    rabbitmq = RabbitMQClient( 
            username='it490admin', 
            password='password'
            )
    rabbitmq.connect()
    rabbitmq.declare_queue("favorite")
    son_user_data = json.dumps(data)
    rabbitmq.send_message(exchange="", routing_key="favorite", body=son_user_data)
    rabbitmq.close()

    return render_template('savedidea.html')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    weather = request.form.get('weather')
    time_of_day = request.form.get('time_of_day')
    activity = request.form.get('activity')
    preferences = request.form.get('preferences')
    budget = request.form.get('budget')
    location = request.form.get('location')

    weather_data = get_weather_data(location, WEATHER_API_KEY)
    if not weather_data:
        error_message = f"Invalid location: {location}. Please try again with a valid location."
        return render_template('error.html', error_message=error_message)

    yelp_data = get_yelp_data(location, activity, preferences)
    if not yelp_data:
        error_message = f"No recommendations found for the given location and activity. Please try again with different inputs."
        return render_template('error.html', error_message=error_message)

    # Use yelp_data as a list of recommendations
    recommendations = yelp_data

    # Check if current weather matches the user's preferred weather
    current_weather = weather_data.get("weather", [{}])[0].get("main", "").lower()
    weather_warning = None
    if weather == "sunny" and "clear" not in current_weather:
        weather_warning = "The current weather does not match your preferred sunny weather."
    elif weather == "rainy" and "rain" not in current_weather:
        weather_warning = "The current weather does not match your preferred rainy weather."
    elif weather == "cloudy" and "clouds" not in current_weather:
        weather_warning = "The current weather does not match your preferred cloudy weather."

    return render_template('recommendation.html', recommendations=recommendations, warning=weather_warning)




if __name__ == '__main__':
	app.run(host='localhost', port=7007)

