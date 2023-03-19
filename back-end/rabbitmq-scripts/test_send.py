#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('brian','password')
parameters = pika.ConnectionParameters('10.0.0.218',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.basic_publish(exchange='fe2be', routing_key='test', body='hello')
connection.close()

