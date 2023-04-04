import pika
import sys
import json
from Receive import receive
from Send import send
#import mysql.connector as mariadb
import hashlib

def hash_password(password):
    """Hashes a given password using SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def main():
    open_connection = receive(
        "b-6a393830-73ed-476c-9530-c0b5029109d0",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )    
    result = open_connection.consume_messages("signin")
    open_connection.close()
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

    open_connection = send(
        "b-6a393830-73ed-476c-9530-c0b5029109d0",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )
    open_connection.declare_queue("signin2db")
    data_to_db = json.dumps(signin_data)
    open_connection.send_message(exchange="", routing_key="signin2db", body=data_to_db)
    open_connection.close() 

    open_connection = receive(
        "b-6a393830-73ed-476c-9530-c0b5029109d0",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )    
    result1 = open_connection.consume_messages("userexists")
    open_connection.close() 
    print(result1)

    global tempBool
    for x in result1:
        if x == 'reply':
            if result1[x] == 'True':
                tempBool = True
            else:
                tempBool = False

    tempDict = {}
    if(tempBool == True):
        tempDict = result1.copy()
        tempDict["Yes"] = []
        tempDict["Yes"].append("Yes")
        open_connection = send(
                    "b-6a393830-73ed-476c-9530-c0b5029109d0",
                    "it490admin",
                    "c7dvcdbtgpue",
                    "us-east-1"
                )
        open_connection.declare_queue("redirectlogin")
        data_to_fe = json.dumps(tempDict)
        open_connection.send_message(exchange="", routing_key="redirectlogin", body=data_to_fe)
        open_connection.close()
    else:
        tempDict = {"No":"No"}
        open_connection = send(
                    "b-6a393830-73ed-476c-9530-c0b5029109d0",
                    "it490admin",
                    "c7dvcdbtgpue",
                    "us-east-1"
        )
        open_connection.declare_queue("redirectlogin")
        data_to_fe = json.dumps(tempDict)
        open_connection.send_message(exchange="", routing_key="redirectlogin", body=data_to_fe)
        open_connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
