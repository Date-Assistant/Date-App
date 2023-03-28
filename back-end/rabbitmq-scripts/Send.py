#!/usr/bin/env python3
import pika
from pika.exchange_type import ExchangeType


class send:
        def __init__(self,ip_addr,port,username,password,vhost,exchange,queue,routing_key,exchange_type):
          self.ip_addr = ip_addr
          self.port = port
          self.username = username
          self.password = password
          self.vhost = vhost
          self.exchange = exchange
          self.exchange_type = exchange_type
          self.routing_key = routing_key
          self.queue = queue
          self.credentials = pika.PlainCredentials(self.username, self.password)
          self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ip_addr,port=self.port,credentials=self.credentials,virtual_host=self.vhost,socket_timeout=300))
          self.channel = self.connection.channel()


        def send_message(self, message):
          self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
          self.channel.queue_declare(queue=self.queue, durable=True)
          self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)

          self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

          self.channel.close()
          self.connection.close()
