import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import hashlib
import time

def main():
    start_time = time.time()
    fname = ''
    lname = ''
    email = ''
    passwd = ''
    phone = ''
    address = ''
    zip = ''
    receive_emails = ''
    temp = {'first_name': '','last_name':'','email':'','password':'','phone':'','address':'','zip_code':'','receive_emails':''}

    rabbitmq = RabbitMQClient(
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            break  
        result = rabbitmq.consume_messages("register")
        rabbitmq.close()
        # print(result)

        for x in result:
            if(x == 'first_name'):
                fname = result[x]
                if('first_name' in temp and temp['first_name'] == fname):
                    pass
                elif(temp['first_name'] == fname):
                    pass
                else:
                    temp['first_name'] = fname
            elif(x == 'last_name'):
                lname = result[x]
                if('last_name' in temp and temp['last_name'] == lname):
                    pass
                elif(temp['last_name'] == lname):
                    pass
                else:
                    temp['last_name'] = lname
            elif(x == 'email'):
                email = result[x]
                if(temp['email'] in temp and temp['email'] == email):
                    pass
                elif(temp['email'] == email):
                    pass
                else:
                    temp['email'] = email
            elif(x == 'password'):
                passwd = result[x]
                if('password' in temp and temp['password'] == passwd):
                    pass
                elif(temp['password'] == passwd):
                    pass
                else:
                    temp['password'] = passwd
                    # Hash the password using SHA-256
                    hashed_password = hashlib.sha256(passwd.encode("utf-8")).hexdigest()
                    temp['password'] = str(hashed_password)
            elif(x == 'phone'):
                phone = result[x]
                if('phone' in temp and temp['phone'] == phone):
                    pass
                elif(temp['phone'] == phone):
                    pass
                else:
                    temp['phone'] = phone
            elif(x == 'address'):
                address = result[x]
                if('address'in temp and temp['address'] == address):
                    pass
                elif(temp['address'] == address):
                    pass
                else:
                    temp['address'] = address
            elif(x == 'zip_code'):
                zip = result[x]
                if('zip_code' in temp and temp['zip_code'] == zip):
                    pass
                elif(temp['zip_code'] == zip):
                    pass
                else:
                    temp['zip_code'] = zip
            elif(x == 'receive_emails'):
                if(result[x] == 'on'):
                    receive_emails = 'on'
                else:
                    receive_emails = 'off'
                if('receive_emails' in temp and temp['receive_emails'] == receive_emails):
                    pass
                elif(temp['receive_emails'] == receive_emails):
                    pass
                else:
                    temp['receive_emails'] = receive_emails
        print(temp['first_name'])
            
        sqlInsert = "INSERT INTO users (fname,lname,email,password,phone,address,zipcode,received_emails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        userTuple = (temp['first_name'],temp['last_name'],temp['email'],str(temp['password']),temp['phone'],temp['address'],temp['zip_code'],temp['receive_emails'])
        registration_data = {
            'insertStatement': sqlInsert,
            'userInfoTuple' : userTuple
        }
        
        rabbitmq.connect()
        rabbitmq.declare_queue("register2db")
        data_to_db = json.dumps(registration_data)
        rabbitmq.send_message(exchange="", routing_key="register2db", body=data_to_db)
        rabbitmq.close()
        time.sleep(1)  

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
