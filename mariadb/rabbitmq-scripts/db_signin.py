import pika
import sys
import json
from Receive import receive
from Send import send
#import mysql.connector as mariadb

return_string = ''
fname = ''
lname= ''
return_dict = {}
global sqlInsert
global userTuple
sqlInsert = ''
userTuple = ()

# mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
# cursor = mariadb_connection.cursor()

def main():
    open_connection = receive(
        "b-ab0030a8-c56e-4e76-90d1-be3ca3d76e12",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )    
    result = open_connection.consume_messages("signin2db")
    open_connection.close()
    # print(result)

"""
    for x in result:
        if(x == 'insertStatement'):
            sqlInsert = result[x]
        elif(x == 'userInfoTuple'):
            userTuple = result[x]

    cursor.execute(sqlInsert,userTuple)
    results = cursor.fetchall()

    if not results:
        return_dict = {
            'fname':'null',
            'lname':'null',
            'password': 'null',
            'reply':'false'
        }
    else:
        for row in results:
            if row[2] == userTuple[0] and row[3] == userTuple[1]:
                fname = row[0]
                lname = row[1]
                hpassword = row[3]
                return_string = 'True'
                pass
        return_dict = {'fname':fname,'lname':lname,'reply':return_string,'password':hpassword}

    db_to_backend = Send.send(ip_addr,port,username,password,vhost,sending_exchange,sending_queue,sending_routing_key,db_exchange_type)
    data_to_be = json.dumps(return_dict)
    db_to_backend.send_message(data_to_be)
     
    db_receive.close()
    db_to_backend.close()

    
    
    cursor.close()
    #mariadb_connection.commit()
"""    
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
