#!/usr/bin/env python
import pika
import json

credentials = pika.PlainCredentials('brian','password')
parameters = pika.ConnectionParameters('10.0.0.218',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

message = {'hello':'test'}

channel = connection.channel()
json_user_data = json.dumps(message)

channel.basic_publish(exchange='fe2be', routing_key='fe2be', body='hello')
connection.close()

