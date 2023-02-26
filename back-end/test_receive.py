#!/usr/bin/env python
import pika, sys

def main():
    credentials = pika.PlainCredentials('brian','password')
    parameters = pika.ConnectionParameters('10.241.51.24',5672,'cherry_broker',credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='front-end')

    def callback(ch, method, properties, body):
        print(" [x] Received %r " % body)
        tempList = []
        tempList.append(body)
        file1 = open("file.txt","w")
        for x in tempList:
            file1.write(x.decode('utf-8','strict') + "\n ")
        file1.close()

    channel.basic_consume(queue='front-end',
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

