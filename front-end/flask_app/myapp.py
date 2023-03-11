from flask import Flask, render_template, request, url_for, flash, redirect
import pika

app = Flask(__name__)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
'''
credentials = pika.PlainCredentials('thebigrabbit','it490')
parameters = pika.ConnectionParameters('10.0.0.218',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='This is register send test')
'''

@app.route('/')
def index():
    return render_template('index.html')

# ...

@app.route('/create/', methods=('GET', 'POST'))
def create():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if not title:
                flash('Title is required!')
            elif not content:
                flash('Content is required!')
            else:
                messages.append({'title': title, 'content': content})
                '''
                channel.basic_publish(exchange='',
                routing_key='This is register send test',
                body = '%s : %s' % (title,content))
                connection.close()
                '''
                return redirect(url_for('index'))

        return render_template('create.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Retrieve the form data
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        zip = request.form['zip']
        email_toggle = request.form.get('email-toggle', 'off')

        # Create a dictionary to store the form data
        user_data = {
            'first_name': fname,
            'last_name': lname,
            'email': email,
            'phone': phone,
            'address': address,
            'zip_code': zip,
            'receive_emails': email_toggle
        }

        # Print the form data
        print(user_data)

        # TODO: Add code to store the data in a database or message queue

    return render_template('register.html')


if __name__ == '__main__':
	app.run(host='localhost', port=7007)

