#!/usr/bin/env python3
import pika
import json
from pika.exchange_type import ExchangeType

class recieve:
      def __init__(self,ip_addr,port,username,password,vhost,queue,routing_key,exchange,exchange_type):
            self.ip_addr = ip_addr
            self.port = port
            self.username = username
            self.password = password
            self.vhost = vhost
            self.exchange = exchange
            self.exchange_type = exchange_type
            self.routing_key = routing_key
            self.queue = queue
   
      def receive_message(self,data):
         self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ip_addr,port=self.port,credentials=pika.PlainCredentials(username=self.username,password=self.password),virtual_host=self.vhost,socket_timeout=300))
         self.channel = self.connection.channel()

         self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
         self.channel.queue_declare(queue=self.queue, durable=True)
         self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)

         def callback(ch, method, properties, body):
            data.update(json.loads(body))
            

         self.channel.basic_consume(queue=self.queue,
         on_message_callback=callback,
         auto_ack=True)


         print(' [*] Waiting for messages.')
         try:
            self.channel.start_consuming()
         except:
            self.channel.stop_consuming()

         self.channel.close()
         self.connection.close()

         return data
         

         
