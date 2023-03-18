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
db_queue= 'dbqueue'
exchange = ''
db_exchange_type = 'direct'
db_routing_key = 'dbqueue'


mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    db_receive = Receive.recieve(ip_addr,port,username,password,vhost,db_queue,db_routing_key,db_exchange_type)
    backend_data = {}
    result = db_receive.receive_from_backend(db_queue,backend_data)
    fname = ''
    lname = ''
    email = ''
    passwd = ''
    phone = ''
    address = ''
    zip = 0
    receive_emails = 0

    for x in result:
        if(x == 'first_name'):
            fname = result[x]
        elif(x == 'last_name'):
            lname = result[x]
        elif(x == 'email'):
            email = result[x]
        elif(x == 'password'):
            passwd = result[x]
        elif(x == 'phone'):
            phone = result[x]
        elif(x == 'address'):
            address = result[x]
        elif(x == 'zip_code'):
            print(type(result[x]))
        elif(x == 'receive_emails'):
            if(result[x] == 'on'):
                receive_emails = 1
            else:
                receive_emails = 0
        sqlInsert = "INSERT INTO users (fname,lname,email,password,phone,address,received_emails) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        infoTuple = (fname,lname,email,passwd,phone,address,receive_emails)
        cursor.execute(sqlInsert,infoTuple)
        mariadb_connection.commit()
    
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)