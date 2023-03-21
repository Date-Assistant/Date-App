import pika
import sys
import json
import Receive
import Send
import mysql.connector as mariadb


username = 'brian'
password = 'password'
ip_addr = '10.0.0.218'
port = 5672
vhost = 'cherry_broker'
db_queue= 'dbregistration'
exchange = 'be2db'
db_exchange_type = 'direct'
db_routing_key = 'dbregistration'


mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    db_receive = Receive.recieve(ip_addr,port,username,password,vhost,exchange,db_queue,db_routing_key,db_exchange_type)
    backend_data = {}
    result = db_receive.receive_message(backend_data)
    for x in result:
        print(x)
    #cursor.execute(sqlInsert,infoTuple)
    #mariadb_connection.commit()
    
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
