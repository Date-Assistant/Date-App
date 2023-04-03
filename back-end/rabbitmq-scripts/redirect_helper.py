# Just a Helper to test Redirection on Signin for NOW not PROD

import pika
import sys
import json
from Receive import receive
from Send import send

def main():
    open_connection = send(
        "b-ab0030a8-c56e-4e76-90d1-be3ca3d76e12",
        "it490admin",
        "c7dvcdbtgpue",
        "us-east-1"
    )
    open_connection.declare_queue("redirectlogin")
    dict = {"No": "No"}
    dict = json.dumps(dict)
    open_connection.send_message(exchange="", routing_key="redirectlogin", body=dict)
    open_connection.close()  

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
