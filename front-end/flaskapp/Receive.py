import json
from basicClient import BasicPikaClient

class receive(BasicPikaClient):
    def __init__(self, rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, region):
        super().__init__(rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, region)
        self.message = None


    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            # print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return body
        else:
            print('No message returned')

    def close(self):
        self.channel.close()
        self.connection.close()

    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            self.message = body.decode('utf-8')
            self.message = json.loads(self.message)
            # print(self.message)
            print(" [x] Received %r" % self.message)
            self.channel.stop_consuming() # stop consuming after first message is received

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

        return self.message
