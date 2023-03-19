#!/usr/bin/env python3
import pika
import json

class recieve:
      def __init__(self,ip_addr,port,username,password,vhost,exchange,que):
            self.ip_addr = ip_addr
            self.port = port
            self.username = username
            self.password = password
            self.vhost = vhost
            self.exchange = exchange
            self.queue = que
            self.credentials = pika.PlainCredentials(self.username, self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
            self.channel = self.connection.channel()
      
      def receive_from_frontend(self,copyDict):
         self.channel.queue_declare(queue=self.queue, exclusive=True)
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
            return 'consumed'
            

         self.channel.basic_consume(queue=self.queue,
         on_message_callback=callback,
         auto_ack=True)


         print(' [*] Waiting for messages.')
         self.channel.start_consuming()

         return self.copyDict
      
      
         

         
