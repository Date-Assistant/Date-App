import pika
import sys
import json
from Receive import receive
from Send import send
#import mysql.connector as mariadb

# mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
# cursor = mariadb_connection.cursor()

def main():
    open_connection = receive(
        "b-ab0030a8-c56e-4e76-90d1-be3ca3d76e12",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )    
    result = open_connection.consume_messages("register2db")
    open_connection.close()
    print(result)

"""
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
"""
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
