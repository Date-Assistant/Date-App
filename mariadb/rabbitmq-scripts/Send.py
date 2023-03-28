import pika

class Send:
    def __init__(self, ip, port, username, password, vhost, exchange, exchange_type):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = None
        self.channel = None
        self.queue = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.ip, self.port, self.vhost, credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type,durable=True)

    def send_message(self, message, routing_key):
        self.connect()
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=message)
        self.close()

    def close(self):
        self.channel.close()
        self.connection.close()

