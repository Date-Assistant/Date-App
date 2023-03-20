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
db_queue= 'signininfo'
exchange = 'be2db'
db_exchange_type = 'direct'
db_routing_key = 'signininfo'


mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    db_receive = Receive.recieve(ip_addr,port,username,password,vhost,exchange,db_queue,db_routing_key,db_exchange_type)
    backend_data = {}
    result = db_receive.receive_from_backend(backend_data)
    email = ''
    passwd = ''
    temp = {'email':'','password':''}

    for x in result:
        if(x == 'email'):
            email = result[x]
            if(temp['email'] in temp and temp['email'] == email):
                pass
            elif(temp['email'] == email):
                pass
            else:
                temp['email'] = email
        elif(x == 'password'):
            passwd = result[x]
            if('password' in temp and temp['password'] == passwd):
                pass
            elif(temp['password'] == passwd):
                pass
            else:
                temp['password'] = passwd
    
    sqlInsert = "INSERT INTO users (fname,lname,email,password,phone,address,zipcode,received_emails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    infoTuple = (temp['first_name'],temp['last_name'],temp['email'],temp['password'],temp['phone'],temp['address'],temp['zip_code'],temp['receive_emails'])
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
