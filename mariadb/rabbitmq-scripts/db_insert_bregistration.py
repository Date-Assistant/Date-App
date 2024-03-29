import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import mysql.connector as mariadb
import time

mariadb_connection = mariadb.connect(host='localhost', user='admin', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    rabbitmq = RabbitMQClient( 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect() 
    result = rabbitmq.consume_messages("businessregister2db")
    rabbitmq.close()
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
