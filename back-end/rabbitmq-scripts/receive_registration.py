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
fe_exchange = 'fe2be'
db_exchange = 'be2db'
fe_declare_queue = 'registration'
fe_routing_key = 'fe2be'
db_routing_key = 'dbqueue'

def main():
    registration_receive = Receive.recieve(ip_addr,port,username,password,vhost,fe_exchange,fe_declare_queue,fe_routing_key)
    frontend_data = {}
    result = registration_receive.receive_from_frontend(frontend_data)

    '''
    back_end_to_db = Send.send(ip_addr,port,username,password,vhost,db_exchange,db_routing_key)
    data_to_db = json.dumps(result)
    back_end_to_db.send_message(data_to_db)
    '''

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)