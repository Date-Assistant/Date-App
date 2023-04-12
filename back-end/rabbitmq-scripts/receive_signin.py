import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
#import mysql.connector as mariadb
import hashlib

def hash_password(password):
    """Hashes a given password using SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def main():
    rabbitmq = RabbitMQClient(
        host='18.234.152.143', 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()   
    result = rabbitmq.consume_messages("signin")
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
    
    sqlInsert = "SELECT fname,lname,email,password FROM users WHERE email = %s AND password = %s"
    infoTuple = (temp['email'], hashed_password)
    signin_data = {
        'insertStatement': sqlInsert,
        'userInfoTuple' : infoTuple
    }

    rabbitmq.connect()
    rabbitmq.declare_queue("signin2db")
    data_to_db = json.dumps(signin_data)
    rabbitmq.send_message(exchange="", routing_key="signin2db", body=data_to_db)
    rabbitmq.close() 

    rabbitmq.connect()
    result1 = rabbitmq.consume_messages("userexists")
    rabbitmq.close() 
    print(result1)

    global tempBool
    lastname = ''
    firstname = ''
    for x in result1:
        if x == 'reply':
            if result1[x] == 'True':
                tempBool = True
            else:
                tempBool = False
        if x == 'fname':
            firstname = result1['fname']
        if x == 'lname':
            lastname = result1['lname']


    tempDict = {}
    if(tempBool == True):
        rabbitmq = send(
                    "b-6a393830-73ed-476c-9530-c0b5029109d0",
                    "it490admin",
                    "c7dvcdbtgpue",
                    "us-east-1"
        )
        tempDict['first_name'] = ''
        tempDict['first_name'] = firstname
        tempDict['last_name'] = ''
        tempDict['last_name'] = lastname
        tempDict['email'] = ''
        tempDict['email'] = temp['email']
        tempDict["Yes"] = ""
        tempDict["Yes"] = "Yes"
        tempDict['password'] = ''
        tempDict['password'] += temp['password']
        rabbitmq.declare_queue("redirectlogin")
        data_to_fe = json.dumps(tempDict)
        rabbitmq.send_message(exchange="", routing_key="redirectlogin", body=data_to_fe)
        rabbitmq.close()
    else:
        tempDict = {"No":"No"}
        rabbitmq.connect()
        rabbitmq.declare_queue("redirectlogin")
        data_to_fe = json.dumps(tempDict)
        rabbitmq.send_message(exchange="", routing_key="redirectlogin", body=data_to_fe)
        rabbitmq.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
