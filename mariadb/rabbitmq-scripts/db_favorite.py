import pika
import sys
import json
import time
from RabbitMQClient import RabbitMQClient
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(host='localhost', user='admin', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()

def main():
    rabbitmq = RabbitMQClient( 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    result = rabbitmq.consume_messages("favorite")
    rabbitmq.close()

    # parse the result
    data = result

    # get the email and place_id from the data
    email = data['email']
    place_id = data['id']

    # find the user id corresponding to the email
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()

    if user_id:
        # if a user id is found, insert the user id and place id into the favorites table
        sqlInsert = "INSERT INTO favorites (user_id, place_id) VALUES (%s, %s)"
        cursor.execute(sqlInsert, (user_id[0], place_id))
        mariadb_connection.commit()
        print("Successfully saved place to favorites for user.")
    else:
        print("User not found.")

    cursor.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)