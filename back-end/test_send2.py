#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('brian','password')
parameters = pika.ConnectionParameters('10.241.51.24',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='Real test')
channel.basic_publish(exchange='',
        routing_key='Real test',
        body = 'Real test for class')
connection.close()

