import pika
import json
import subprocess
import random
import socket

def is_rabbitmq_running(ip, ports=(5672, 15672), timeout=5):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
                print(f"RabbitMQ service is running on {ip}:{port}")
                return True
            except (socket.timeout, ConnectionRefusedError):
                print(f"RabbitMQ service is not running on {ip}:{port}")
                return False

def get_random_online_node():
    timeout=2
    online_nodes = []
    offline_nodes = []

    # List of node IP addresses
    node_list = [
        '172.30.0.140',
        '172.30.0.177',
        '172.30.1.201',
        '10.0.0.203',
        '172.31.15.87'
    ]

    for node in node_list:
        try:
            response = subprocess.run(['ping', '-c', '1', '-W', str(timeout), node], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if response.returncode == 0:
                print(f"Node {node} is GOOD.")
                if is_rabbitmq_running(node):
                    online_nodes.append(node)
                else:
                    offline_nodes.append(node)
            else:
                print(f"Node {node} is BAD.")
                offline_nodes.append(node)
        except Exception as e:
            offline_nodes.append(node)
            print(f"Error pinging node {node}: {e}")
    if online_nodes:
        random_online_node = random.choice(online_nodes)
        return random_online_node
    else:
        print("No online nodes found.")
        return None

ip_addr = get_random_online_node()

class RabbitMQClient:
    def __init__(self, host, username, password, virtual_host='/'):
        self.host = ip_addr
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
            self.message = body.decode('utf-8')
            self.message = json.loads(self.message)
            # print(self.message)
            print(" [x] Received %r" % self.message)
            self.channel.stop_consuming() # stop consuming after first message is received

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

        return self.message