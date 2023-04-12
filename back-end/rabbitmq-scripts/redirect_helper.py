# Just a Helper to test Redirection on Signin for NOW not PROD

import pika
import sys
import json
from RabbitMQClient import RabbitMQClient

def main():
    rabbitmq = RabbitMQClient(
        host='18.234.152.143', 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    rabbitmq.declare_queue("redirectlogin")
    dict = {"No": "No"}
    dict = json.dumps(dict)
    rabbitmq.send_message(exchange="", routing_key="redirectlogin", body=dict)
    rabbitmq.close()  

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
