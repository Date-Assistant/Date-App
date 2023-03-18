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
    zip = ''
    receive_emails = ''
    temp = {}

    for x in result:
        if(x == 'first_name'):
            fname = result[x]
            if(temp['first_name'] in temp):
                pass
            elif(temp['first_name'] == fname):
                pass
            else:
                temp['first_name'] = fname
        elif(x == 'last_name'):
            lname = result[x]
            if(temp['last_name'] in temp):
                pass
            elif(temp['last_name'] == lname):
                pass
            else:
                temp['last_name'] = lname
        elif(x == 'email'):
            email = result[x]
            if(temp['email'] in temp):
                pass
            elif(temp['email'] == email):
                pass
            else:
                temp['email'] = email
        elif(x == 'password'):
            passwd = result[x]
            if(temp['password'] in temp):
                pass
            elif(temp['password'] == passwd):
                pass
            else:
                temp['password'] = passwd
        elif(x == 'phone'):
            phone = result[x]
            if(temp['phone'] in temp):
                pass
            elif(temp['phone'] == phone):
                pass
            else:
                temp['phone'] = phone
        elif(x == 'address'):
            address = result[x]
            if(temp['address'] in temp):
                pass
            elif(temp['address'] == address):
                pass
            else:
                temp['address'] = address
        elif(x == 'zip_code'):
            zip = result[x]
            if(temp['zip_code'] in temp):
                pass
            elif(temp['zip_code'] == zip):
                pass
            else:
                temp['zip_code'] = zip
        elif(x == 'receive_emails'):
            if(result[x] == 'on'):
                receive_emails = 'on'
            else:
                receive_emails = 'off'
            if(temp['receive_emails'] in temp):
                pass
            elif(temp['receive_emails'] == receive_emails):
                pass
            else:
                temp['receive_emails'] = receive_emails
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