#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('thebigrabbit','it490')
parameters = pika.ConnectionParameters('10.241.51.24',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='Lap this is a test to receive')
channel.basic_publish(exchange='',
        routing_key='Lap this is a test to receive',
        body = 'Hello')
connection.close()

