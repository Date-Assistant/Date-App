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
front_end_queue= 'queue1'
signin_queue = 'testqueue'
front_end_exchange = 'fe2be'
front_end_exchange_type = 'direct'
front_end_routing_key = 'signin'

db_queue= 'dbqueue'
db_exchange = 'be2db'
db_exchange_type = 'direct'
db_routing_key = 'signininfo'

def main():
    backend_receive = Receive.recieve(ip_addr,port,username,password,vhost,signin_queue,front_end_routing_key,front_end_exchange,front_end_exchange_type)
    frontend_data = {}
    result = backend_receive.receive_from_frontend(frontend_data)

    back_end_to_db = Send.send(ip_addr,port,username,password,vhost,db_exchange,db_queue,db_routing_key,db_exchange_type)
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