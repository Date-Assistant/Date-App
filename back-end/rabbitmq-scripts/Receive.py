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
            self.credentials = pika.PlainCredentials(self.username, self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
            self.channel = self.connection.channel()
      
      def close(self):
          if self.channel is not None and self.channel.is_open:
            self.channel.close()
          if self.connection is not None and self.connection.is_open:
            self.connection.close()

      def receive_message(self,copyDict):
         #self.channel.exchange_declare(exchange=self.exchange, durable=True,exchange_type=ExchangeType.direct)
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
            callback_dict = { 'frontend' : x}
            global newDict
            newDict = json.loads(callback_dict['frontend'])
            for key, value in newDict.items():
               self.copyDict[key] = value
            print('consumed')
            

         self.channel.basic_consume(queue=self.queue,
         on_message_callback=callback,
         auto_ack=True)


         print(' [*] Waiting for messages.')
         try:
            self.channel.start_consuming()
         except:
            self.channel.stop_consuming()

         return self.copyDict
         

         
