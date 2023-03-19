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
exchange_type = 'direct'
queues_to_declare = {'register': 'registration_received'}
routing_keys = {'front_end':'registration_form','db':'dbqueue'}
exchanges = {'frontend':'fe2be','database':'be2db'}

def main():
    registration_receive = Receive.recieve(ip_addr,port,username,password,vhost,exchanges['frontend'],queues_to_declare['register'],routing_keys['front_end'],exchange_type)
    frontend_data = {}
    result = registration_receive.receive_from_frontend(frontend_data)


    back_end_to_db = Send.send(ip_addr,port,username,password,vhost,exchanges['database'],routing_keys['db'],exchange_type)
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