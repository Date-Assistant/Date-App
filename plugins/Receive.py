#!/usr/bin/env python3
import pika

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
        
  def receive_from_frontend(self,queue):
  # create receive_registration.py that subscribes to same exchange and routing key from /register route in myapp.py
  	self.channel.queue_declare(queue=self.queue)

     def callback(ch, method, properties, body):
        print(" [x] Received %r " % body)

    self.channel.basic_consume(queue=self.queue,
    on_message_callback=callback,
    auto_ack=True)

    print(' [*] Waiting for messages.')
    self.channel.start_consuming()
