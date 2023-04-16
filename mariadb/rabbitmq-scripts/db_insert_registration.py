import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import mysql.connector as mariadb
import time

mariadb_connection = mariadb.connect(host='localhost', user='admin', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    start_time = time.time()
    rabbitmq = RabbitMQClient( 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            break  
        result = rabbitmq.consume_messages("register2db")
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
        time.sleep(1)
                

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
