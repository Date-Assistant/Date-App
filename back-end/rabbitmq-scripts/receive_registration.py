import pika
import sys
import json
import Receive
import Send

username = 'brian'
password = 'password'
ip_addr = '10.0.0.218'
port = 5672
vhost = 'cherry_broker'
queue= 'hello'
exchange = ''
exchange_type = 'direct'
routing_key = 'hello'

def main():
		backend_receive = Receive.recieve(ip_addr,port,username,password,vhost,queue,routing_key,exchange_type)
		backend_receive.receive_from_frontend(queue)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)