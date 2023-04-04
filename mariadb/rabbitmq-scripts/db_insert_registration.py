import pika
import sys
import json
from Receive import receive
from Send import send
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(host='it490database.canztlnjai3e.us-east-1.rds.amazonaws.com', user='admin', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    open_connection = receive(
        "b-6a393830-73ed-476c-9530-c0b5029109d0",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )    
    result = open_connection.consume_messages("register2db")
    open_connection.close()
    print(result)


    for x in result:
        if(x == 'insertStatement'):
            sqlInsert = result[x]
        elif(x == 'userInfoTuple'):
            userTuple = result[x]
    try:
        cursor.execute(sqlInsert,userTuple)
        mariadb_connection.commit()
    except:
        tempDict = {'error':'error inserting into db'}
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
