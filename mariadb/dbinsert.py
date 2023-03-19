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
be_received_queue = 'be2db'
be_received_exchange = 'be2db'
routing_key = 'be2db'


mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    db_receive = Receive.recieve(ip_addr,port,username,password,vhost,be_received_exchange,be_received_queue,routing_key)
    backend_data = {}
    result = db_receive.receive_from_backend(backend_data)
    fname = ''
    lname = ''
    email = ''
    passwd = ''
    phone = ''
    address = ''
    zip = ''
    receive_emails = ''
    temp = {'first_name': '','last_name':'','email':'','password':'','phone':'','address':'','zip_code':'','receive_emails':''}

    for x in result:
        if(x == 'first_name'):
            fname = result[x]
            if('first_name' in temp and temp['first_name'] == fname):
                pass
            elif(temp['first_name'] == fname):
                pass
            else:
                temp['first_name'] = fname
        elif(x == 'last_name'):
            lname = result[x]
            if('last_name' in temp and temp['last_name'] == lname):
                pass
            elif(temp['last_name'] == lname):
                pass
            else:
                temp['last_name'] = lname
        elif(x == 'email'):
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
        elif(x == 'phone'):
            phone = result[x]
            if('phone' in temp and temp['phone'] == phone):
                pass
            elif(temp['phone'] == phone):
                pass
            else:
                temp['phone'] = phone
        elif(x == 'address'):
            address = result[x]
            if('address'in temp and temp['address'] == address):
                pass
            elif(temp['address'] == address):
                pass
            else:
                temp['address'] = address
        elif(x == 'zip_code'):
            zip = result[x]
            if('zip_code' in temp and temp['zip_code'] == zip):
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
            if('receive_emails' in temp and temp['receive_emails'] == receive_emails):
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
