import pika

class Send:
    def __init__(self, ip, port, username, password, vhost, exchange, queue,exchange_type):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = None
        self.channel = None
        self.queue = queue

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.ip, self.port, self.vhost, credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type,durable=True)
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)

    def send_message(self, message, routing_key):
        self.connect()
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=message)
        self.close()

    def close(self):
        self.channel.close()
        self.connection.close()

