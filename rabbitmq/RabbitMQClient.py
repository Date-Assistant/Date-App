import pika
import json

class RabbitMQClient:
    def __init__(self, host, username, password, virtual_host='/'):
        self.host = host
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.host, virtual_host=self.virtual_host, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self):
        self.channel.close()
        self.connection.close()

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")
    
    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

"""
    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            self.message = body.decode('utf-8')
            self.message = json.loads(self.message)
            # print(self.message)
            print(" [x] Received %r" % self.message)
            self.channel.stop_consuming() # stop consuming after first message is received

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

        return self.message
"""


# Example usage of sending:
"""
rabbitmq = RabbitMQClient(
    host='18.234.152.143', 
    username='it490admin', 
    password='password'
)
rabbitmq.connect()
rabbitmq.declare_queue("test2")
rabbitmq.send_message(exchange="", routing_key="test2", body="TEST MESSAGE 2")
rabbitmq.close() 
"""

# Example usage of consuming:
"""
rabbitmq = RabbitMQClient(
    host='18.234.152.143', 
    username='it490admin', 
    password='password'
)
rabbitmq.connect()
rabbitmq.consume_messages("test2")
rabbitmq.close()
"""