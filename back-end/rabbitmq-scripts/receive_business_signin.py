import pika
import sys
import json
import time
from RabbitMQClient import RabbitMQClient
#import mysql.connector as mariadb
import hashlib

def hash_password(password):
    """Hashes a given password using SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def main():
    rabbitmq = RabbitMQClient(
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect() 
    result = rabbitmq.consume_messages("bsignin")
    rabbitmq.close()
    # print(result)

    email = ''
    passwd = ''
    temp = {'email': '', 'password': ''}

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
                tempPass = passwd
                pass
            elif(temp['password'] == passwd):
                tempPass = passwd
                pass
            else:
                temp['password'] = passwd
                tempPass = passwd
    
    hashed_password = hash_password(temp['password'])
    
    sqlInsert = "SELECT bname, email, password FROM businesses WHERE email = %s AND password = %s"
    infoTuple = (temp['email'], hashed_password)
    signin_data = {
        'insertStatement': sqlInsert,
        'userInfoTuple' : infoTuple
    }

    rabbitmq.connect()
    rabbitmq.declare_queue("bsignin2db")
    data_to_db = json.dumps(signin_data)
    rabbitmq.send_message(exchange="", routing_key="bsignin2db", body=data_to_db)
    rabbitmq.close() 

    rabbitmq.connect()
    result1 = rabbitmq.consume_messages("businessexists")
    rabbitmq.close() 
    print(result1)

    global tempBool
    lastname = ''
    bname = ''
    for x in result1:
        if x == 'reply':
            if result1[x] == 'True':
                tempBool = True
            else:
                tempBool = False
        if x == 'bname':
            bname = result1['bname']


    tempDict = {}
    if(tempBool == True):
        rabbitmq.connect() 
        tempDict['business_name'] = ''
        tempDict['business_name'] = bname
        tempDict['email'] = ''
        tempDict['email'] = temp['email']
        tempDict["Yes"] = ""
        tempDict["Yes"] = "Yes"
        tempDict['password'] = ''
        tempDict['password'] += temp['password']
        rabbitmq.declare_queue("bredirectlogin")
        data_to_fe = json.dumps(tempDict)
        rabbitmq.send_message(exchange="", routing_key="bredirectlogin", body=data_to_fe)
        rabbitmq.close()
    else:
        tempDict = {"No":"No"}
        rabbitmq.connect()
        rabbitmq.declare_queue("bredirectlogin")
        data_to_fe = json.dumps(tempDict)
        rabbitmq.send_message(exchange="", routing_key="bredirectlogin", body=data_to_fe)
        rabbitmq.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
