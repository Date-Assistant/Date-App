import pika
import sys
import json
sys.path.append('../../plugins/')
import plugins.Receive as receive
import plugins.Send as send

username = 'thebigrabbit'
password = 'it490'
ip_addr = '10.0.0.218'
port = 5672
vhost = 'cherry_broker'
queue= 'hello'
exchange = ''
exchange_type = 'direct'
routing_key = 'hello'

def main():
	try:
		backend_receive = receive(ip_addr,port,username,password,vhost,queue,routing_key,exchange_type)
		backend_receive.receive_from_frontend(queue)
	except BaseException:
		print("error")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)