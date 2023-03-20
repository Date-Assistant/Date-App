import pika
import sys
import json
import Message
import Send

username = 'brian'
password = 'password'
ip_addr = '10.0.0.218'
port = 5672
vhost = 'cherry_broker'
front_end_queue= 'hello'
exchange = ''
front_end_exchange_type = 'direct'
front_end_routing_key = 'hello'

db_queue= 'dbqueue'
exchange = ''
db_exchange_type = 'direct'
db_routing_key = 'dbqueue'

def main():
    backend_receive = Message.Messaging(ip_addr,port,username,password,vhost,'fe2be','received','registration.data')
    frontend_data = {}
    backend_receive.receive(frontend_data)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)