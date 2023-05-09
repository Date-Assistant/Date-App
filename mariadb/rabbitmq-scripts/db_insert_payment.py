import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import mysql.connector as mariadb
import time
import hashlib

mariadb_connection = mariadb.connect(host='localhost', user='admin', password='password', port='3306', database='IT490')
cursor = mariadb_connection.cursor()

def encrypt_info(info):
    # encrypt the card number and cvc using SHA256
    return hashlib.sha256(info.encode()).hexdigest()

def main():
    rabbitmq = RabbitMQClient( 
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect() 
    result = rabbitmq.consume_messages("payment2db")  # consume from the payment2db queue
    rabbitmq.close()
    print(result)

    for x in result:
        if(x == 'userInfoTuple'):
            userTuple = result[x]

    name = userTuple[0]  # Get the name from the tuple
    userTuple[2] = str(userTuple[2])  # Encrypt the card number
    userTuple[3] = str(userTuple[3])  # Encrypt the cvc

    # Check if the name is in the users table
    cursor.execute("SELECT id FROM users WHERE fname = %s", (name,))
    user_id = cursor.fetchone()

    if user_id:
        # If the name is in the users table, insert into userpayment table
        userTuple[0] = user_id[0]  # Replace the name with the user_id in the tuple
        sqlInsert = "INSERT INTO userpayment (cardholder_name, card_number, expiration_date, cvc, saveCardInfo) VALUES (%s, %s, %s, %s, %s)"
    else:
        # If the name is not in the users table, check the businesses table
        cursor.execute("SELECT id FROM businesses WHERE bname = %s", (name,))
        business_id = cursor.fetchone()

        if business_id:
            # If the name is in the businesses table, insert into businesspayment table
            userTuple[0] = business_id[0]  # Replace the name with the business_id in the tuple
            sqlInsert = "INSERT INTO businesspayment (cardholder_name, card_number, expiration_date, cvc, saveCardInfo) VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor.execute(sqlInsert, userTuple)
        mariadb_connection.commit()
    except Exception as e:
        print("Error:", str(e))
        tempDict = {'error':'error inserting into db'}

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(1)
