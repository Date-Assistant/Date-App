import pika
import sys
import json
import Receive
import Send

username = 'brian'
password = 'password'
ip_addr = '10.0.0.218'
port = 5672
vhost = 'cherry_broker'
signin_queue = 'signin'
front_end_exchange = 'fe2be'
front_end_exchange_type = 'direct'
front_end_routing_key = 'signin'

db_queue= 'signininfo'
db_exchange = 'be2db'
db_exchange_type = 'direct'
db_routing_key = 'signininfo'

receiving_userexist_exchange = 'db2be'
userexist_routing_key = 'userexists'
userexist_queue = 'userexists'

def main():
    backend_receive = Receive.recieve(ip_addr,port,username,password,vhost,signin_queue,front_end_routing_key,front_end_exchange,front_end_exchange_type)
    frontend_data = {}
    result = backend_receive.receive_message(frontend_data)

    email = ''
    passwd = ''
    temp = {'email':'','password':''}

    for x in result:
        if(x == 'email'):
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
    
    sqlInsert = "SELECT email, password FROM users WHERE email = %s AND password = %s"
    infoTuple = (temp['email'],temp['password'])
    signin_data = {
        'insertStatement': sqlInsert,
        'userInfoTuple' : infoTuple
    }

    back_end_to_db = Send.send(ip_addr,port,username,password,vhost,db_exchange,db_queue,db_routing_key,db_exchange_type)
    data_to_db = json.dumps(signin_data)
    back_end_to_db.send_message(data_to_db)

    receive_user_exists = Receive.recieve(ip_addr,port,username,password,vhost,userexist_queue,userexist_routing_key,receiving_userexist_exchange,front_end_exchange_type)
    userexists_data = {}
    result = receive_user_exists.receive_message(userexists_data)
    print(result)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except:
            sys.exit(0)