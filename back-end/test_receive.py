#!/usr/bin/env python
import pika, sys

def main():
    credentials = pika.PlainCredentials('thebigrabbit','it490')
    parameters = pika.ConnectionParameters('10.241.51.24',5672,'cherry_broker',credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='Lap this is a test to receive')

    def callback(ch, method, properties, body):
        print(" [x] Received %r " % body)


    channel.basic_consume(queue='Lap this is a test to receive',
    on_message_callback=callback,
    auto_ack=True)

    print(' [*] Waiting for messages.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)

