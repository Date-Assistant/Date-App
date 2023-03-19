#!/usr/bin/env python3
import pika
import json

class recieve:
      def __init__(self,ip_addr,port,username,password,vhost,exchange,que,routing_key):
            self.ip_addr = ip_addr
            self.port = port
            self.username = username
            self.password = password
            self.vhost = vhost
            self.routing_key = routing_key
            self.exchange = exchange
            self.queue = que
            self.credentials = pika.PlainCredentials(self.username, self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
            self.channel = self.connection.channel()
      
      def receive_from_frontend(self,copyDict):
         result = self.channel.queue_declare(queue=self.queue, exclusive=True)
         queue_name = result.method.queue
         channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.routing_key)
         self.copyDict = copyDict

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
            

         self.channel.basic_consume(queue=queue_name,
         on_message_callback=callback,
         auto_ack=True)


         print(' [*] Waiting for messages.')
         self.channel.start_consuming()

         return self.copyDict
      
      
         

         
