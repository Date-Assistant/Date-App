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
    result = rabbitmq.consume_messages("get_favorites")
    rabbitmq.close()

    # parse the result
    data = result

    # get the email from the data
    email = data['email']

    # find the user id corresponding to the email
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()

    if user_id:
        # if a user id is found, fetch the saved places
        cursor.execute("SELECT place_id FROM favorites WHERE user_id = %s", (user_id[0],))
        saved_places = [item[0] for item in cursor.fetchall()]

        # send the saved places back to the front end
        rabbitmq.connect()
        rabbitmq.declare_queue("favorites_result")
        result_data = {'email': email, 'saved_places': saved_places}
        json_result_data = json.dumps(result_data)
        rabbitmq.send_message(exchange="", routing_key="favorites_result", body=json_result_data)
        rabbitmq.close()

        print("Successfully retrieved saved places for user.")
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
