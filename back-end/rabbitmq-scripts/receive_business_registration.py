import pika
import sys
import json
from RabbitMQClient import RabbitMQClient
import hashlib
import time

def main():
    fname = ''
    lname = ''
    email = ''
    passwd = ''
    phone = ''
    address = ''
    zip = ''
    receive_emails = ''
    discountCode = ''
    membership_type = ''
    temp = {'business_name': '','owner_name':'','email':'','password':'','phone':'','address':'','zip_code':'','receive_emails':'', 'discountCode':'','membership_type' : ''}

    rabbitmq = RabbitMQClient(
        username='it490admin', 
        password='password'
    )
    rabbitmq.connect()
    result = rabbitmq.consume_messages("register2")
    rabbitmq.close()
    # print(result)

    for x in result:
        if(x == 'business_name'):
            fname = result[x]
            if('business_name' in temp and temp['business_name'] == fname):
                pass
            elif(temp['business_name'] == fname):
                pass
            else:
                temp['business_name'] = fname
        elif(x == 'owner_name'):
            lname = result[x]
            if('owner_name' in temp and temp['owner_name'] == lname):
                pass
            elif(temp['owner_name'] == lname):
                pass
            else:
                temp['owner_name'] = lname
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
        
        elif(x == 'discountCode'):
            discountCode = result[x]
            if('discountCode' in temp and temp['discountCode'] == discountCode):
                pass
            elif(temp['discountCode'] == discountCode):
                pass
            else:
                temp['discountCode'] = discountCode

        elif(x == 'membership_type'):
            membership_type = result[x]
            if('membership_type' in temp and temp['membership_type'] == membership_type):
                pass
            elif(temp['membership_type'] == membership_type):
                pass
            else:
                temp['membership_type'] = membership_type
    print(temp['business_name'])
        
    sqlInsert = "INSERT INTO businesses (bname,oname,email,password,phone,address,zipcode,received_emails,discount,membership) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    userTuple = (temp['business_name'],temp['owner_name'],temp['email'],str(temp['password']),temp['phone'],temp['address'],temp['zip_code'],temp['receive_emails'],temp['discountCode'],temp['membership_type'])
    registration_data = {
        'insertStatement': sqlInsert,
        'userInfoTuple' : userTuple
    }
    
    rabbitmq.connect()
    rabbitmq.declare_queue("businessregister2db")
    data_to_db = json.dumps(registration_data)
    rabbitmq.send_message(exchange="", routing_key="businessregister2db", body=data_to_db)
    rabbitmq.close()  

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)
