import pika
import json
import time
import os

class Messaging:
    def __init__(self,ip_addr,port,username,password,vhost,exchange,queue,routing_key):
            self.ip_addr = ip_addr
            self.port = port
            self.username = username
            self.password = password
            self.vhost = vhost
            self.exchange = exchange
            self.queue = queue
            self.routing_key = routing_key
            self.credentials = pika.PlainCredentials(self.username, self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port, self.vhost, self.credentials))
            self.channel = self.connection.channel()

    def send(self, data):
          # self.channel.exchange_declare(exchange='', exchange_type='fanout')
            self.data = data
            self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=self.routing_key,
                    properties=pika.BasicProperties(
                    reply_to=self.queue),
                    body=self.message)
            print(f"Sent message: {self.message}")


    def receive(self,copyDict):
            self.copyDict = copyDict
            self.channel.queue_declare(queue=self.queue)
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)
            def callback(ch, method, properties, body):
                global bodyResult
                bodyResult = body
                x = bodyResult.decode('utf-8','strict')
                callback_dict = { self.ip_addr : x}
                global newDict
                newDict = json.loads(callback_dict[self.ip_addr])
                for key, value in newDict.items():
                    self.copyDict[key] = value
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print('consumed')
                self.connection.close()
            
            self.channel.basic_consume(queue=self.routing_key,
            on_message_callback=callback,
            auto_ack=True)

            print(' [*] Waiting for messages.')
            self.channel.start_consuming()
    