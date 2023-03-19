#!/usr/bin/env python3
import pika


class send:
        def __init__(self,ip_addr,port,username,password,vhost,exchange,routing_key):
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
          self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
          self.channel = self.connection.channel()

        def send_message(self, message):
          # self.channel.exchange_declare(exchange='', exchange_type='fanout')
          self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
