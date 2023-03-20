#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('brian','password')
parameters = pika.ConnectionParameters('10.0.0.218',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
exchange = 'fe2be'
routing_key = 'registration.data'

channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    properties=pika.BasicProperties(
                    reply_to=routing_key),
                    body=message)
