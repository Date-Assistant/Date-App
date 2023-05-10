import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import hashlib
import time

def main():
    rabbitmq = RabbitMQClient(
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    result = rabbitmq.consume_messages("user_queue")  # Consume messages from the user_queue
    rabbitmq.close()

    # Parse the result
    if result:
        payment_data = result

        # Prepare the data for database insertion
        userTuple = (payment_data['name'], payment_data['cardholder_name'], payment_data['card_number'], payment_data['expiration_date'], payment_data['cvc'], payment_data['saveCardInfo'])

        # Create a dictionary to send to the database
        payment_info = {
            'userInfoTuple' : userTuple
        }

        # Send the data to the database
        rabbitmq.connect()
        rabbitmq.declare_queue("payment2db")  # Declare a new queue to send the data to the database
        data_to_db = json.dumps(payment_info)
        rabbitmq.send_message(exchange="", routing_key="payment2db", body=data_to_db)
        rabbitmq.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
