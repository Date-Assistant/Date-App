#!/usr/bin/env python3
import pika
import json

class recieve:
      def __init__(self,ip_addr,port,username,password,vhost,queue,routing_key,exchange_type):
            self.ip_addr = ip_addr
            self.port = port
            self.username = username
            self.password = password
            self.vhost = vhost
            self.exchange_type = exchange_type
            self.routing_key = routing_key
            self.queue = queue
            self.credentials = pika.PlainCredentials(self.username, self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
            self.channel = self.connection.channel()
   

      
      def receive_from_frontend(self,exchange,queue,copyDict):
         # create receive_registration.py that subscribes to same exchange and routing key from /register route in myapp.py
         self.exchange = exchange
         self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type,passive=True)
         result = self.channel.queue_declare(queue=self.queue,exclusive=True)
         queue_name = result.method.queue

         self.channel.queue_bind(
            exchange=self.exchange, queue=queue_name, routing_key=self.routing_key
         )

         '''
         self.channel.queue_declare(queue=self.queue)
         self.copyDict = copyDict
         '''

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
            self.connection.close()
            

         self.channel.basic_consume(queue=queue_name,
         on_message_callback=callback,
         auto_ack=True)


         print(' [*] Waiting for messages.')
         self.channel.start_consuming()

         return self.copyDict
         

         
