from flask import Flask, render_template, request, url_for, flash, redirect
import pika

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd523a32875c96254372519418f55af57b892afc7b7e4401f'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

credentials = pika.PlainCredentials('thebigrabbit','it490')
parameters = pika.ConnectionParameters('10.241.51.24',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='This is register send test')


@app.route('/')
def index():
    return render_template('index.html', messages=messages)

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
                channel.basic_publish(exchange='',
                routing_key='This is register send test',
                body = '%s : %s' % (title,content))
                connection.close()
                return redirect(url_for('index'))

        return render_template('create.html')


if __name__ == '__main__':
	app.run()

