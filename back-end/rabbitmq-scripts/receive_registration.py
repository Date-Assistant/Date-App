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
front_end_queue= 'hello'
exchange = ''
front_end_exchange_type = 'direct'
front_end_routing_key = 'hello'

db_queue= 'hello'
exchange = ''
db_exchange_type = 'direct'
db_routing_key = 'hello'

def main():
    backend_receive = Receive.recieve(ip_addr,port,username,password,vhost,front_end_queue,front_end_routing_key,front_end_exchange_type)
    frontend_data = {}
    result = backend_receive.receive_from_frontend(front_end_queue,frontend_data)
    back_end_to_db = Send.send(ip_addr,port,username,password,vhost,exchange,db_queue,db_routing_key,db_exchange_type)
    data_to_db = json.dumps(result)
    back_end_to_db.send_message(data_to_db)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)