from secrets import token_hex
from hashlib import sha256
import redis

import jett_chat.DBfn.support as support
import config
from datetime import timedelta

mydb, mycursor = support.get_myql_connectors()
redis_client = redis.Redis()

def insert_token_mysql(uname,token):
    
    existsing_record = mycursor.execute("SELECT uname FROM Token WHERE uname = %s", (uname,))

    if existsing_record:

        mycursor.execute("UPDATE Token SET token = %s WHERE uname = %s", (token, uname))
    else:
        
        mycursor.execute("INSERT into Token VALUES(%s,%s)",(uname,token)) 

    mydb.commit()

def check_if_account_exists(uname):
    mycursor.execute("SELECT uname FROM UserInfo WHERE uname = %s", (uname,))
    user = mycursor.fetchall()
    
    return user

def add_new_user(content):

    mycursor.execute("INSERT into UserInfo values (%s, %s, %s, %s)", (
            content["name"], 
            content["email"], 
            content["phone"], 
            content["uname"]
        )
    )

    mydb.commit()

    mycursor.execute("INSERT INTO Password VALUES (%s, %s)", (
        content["uname"], 
        content["password"]
        )
    )

    mydb.commit()

    if check_if_account_exists(content["uname"]):
        print("User Created")


def delete_user(uname):

    mycursor.execute("DELETE FROM Token WHERE uname = %s", uname)
    mycursor.execute("DELETE FROM Password WHERE uname = %s", uname)
    mycursor.execute("DELETE FROM UserInfo WHERE uname = %s", uname)
    return not check_if_account_exists(uname)

def update_user_info(uname, user_object):
    pass

def update_user_password():
    pass

def get_user_info():
    pass

def check_password(uname, password):

    password_hash = support.get_salted_password_hash(uname, password)
    return True


###### Authentication ###########################################################

# generate token for user and store
def generate_token(uname):

    token = uname + "." + token_hex(64)

    insert_token_mysql(uname, token)
    redis_client.setex(token, timedelta(minutes=10), value=uname)

    return { 

        "uname" : uname,
        "token": token
    }

# check token, make it active by putting it in redis cache
def check_token(token):

    uname = redis_client.get(token).decode()

    if uname: 
        
        redis_client.expire(token, timedelta(minutes=10))
        return uname

    else:
        mycursor.execute("SELECT uname FROM Token WHERE token = %s;", (token,))
        uname = mycursor.fetchall()[0][0]

        if uname: 
            redis_client.expire(token, timedelta(minutes=10))
            return uname

        else: 
            return None

# check password and grant a new user token
def process_login(content):

    uname = content['uname']
    password = content['password']
    
    password_hash = sha256((uname + sha256(password.encode()).hexdigest()).encode()).hexdigest()

    if check_password(uname, password_hash):

        return generate_token(uname)