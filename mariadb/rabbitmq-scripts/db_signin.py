import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import mysql.connector as mariadb

return_string = ''
fname = ''
lname= ''
return_dict = {}
global sqlInsert
global userTuple
sqlInsert = ''
userTuple = ()

mariadb_connection = mariadb.connect(host='it490database.canztlnjai3e.us-east-1.rds.amazonaws.com', user='admin', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    rabbitmq = RabbitMQClient(
        host='18.234.152.143', 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    result = rabbitmq.consume_messages("signin2db")
    rabbitmq.close()
    # print(result)


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

    rabbitmq.connect()
    rabbitmq.declare_queue("userexists")
    data_to_be = json.dumps(return_dict)
    rabbitmq.send_message(exchange="", routing_key="userexists", body=data_to_be)
    rabbitmq.close()

    
    
    cursor.close()
    #mariadb_connection.commit()
  
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
