#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('brian','password')
parameters = pika.ConnectionParameters('10.0.0.218',5672,'cherry_broker',credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
routing_key = 'registration.data'
result_queue = channel.queue_declare(queue=routing_key, exclusive=True).method.queue
print(result_queue)
