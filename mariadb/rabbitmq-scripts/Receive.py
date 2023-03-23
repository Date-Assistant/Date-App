#!/usr/bin/env python3
import pika
import json
from pika.exchange_type import ExchangeType


class recieve:
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
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
            self.channel = self.connection.channel()
   

      
      def receive_message(self,copyDict):
         self.channel.exchange_declare(exchange=self.exchange, durable=True, exchange_type=ExchangeType.direct)
         # create receive_registration.py that subscribes to same exchange and routing key from /register route in myapp.py
         self.channel.queue_declare(queue=self.queue)
         self.copyDict = copyDict
         self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)

         def get_dict(dict,otherDict):
            for key, value in dict.items():
               otherDict[key] = value
            return otherDict

         def callback(ch, method, properties, body):
            global bodyResult
            bodyResult = body
            x = bodyResult.decode('utf-8','strict')
            callback_dict = { 'backend' : x}
            global newDict
            newDict = json.loads(callback_dict['backend'])
            for key, value in newDict.items():
               self.copyDict[key] = value
            print('consumed')
            self.connection.close()
            

         self.channel.basic_consume(queue=self.queue,
         on_message_callback=callback,
         auto_ack=True)


         print(' [*] Waiting for messages.')
         self.channel.start_consuming()

         return self.copyDict
      
      
         

         