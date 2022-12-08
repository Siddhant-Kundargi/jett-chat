from secrets import token_hex
from hashlib import sha256

from jett_chat.DBfn import support
from datetime import timedelta

from jett_chat import mysql_connector, mongodb_connector, redis_client
mysql_cursor = mysql_connector.cursor()

def insert_token_mysql(uname,token):
    
    mysql_cursor.execute("SELECT uname FROM Token WHERE uname = %s", (uname,))
    existing_record = mysql_cursor.fetchall()

    if existing_record:

        mysql_cursor.execute("UPDATE Token SET token = %s WHERE uname = %s", (token, uname))
    else:
        
        mysql_cursor.execute("INSERT into Token VALUES(%s,%s)",(uname,token)) 

    mysql_connector.commit()

def check_if_account_exists(uname):

    mysql_cursor.execute("SELECT uname FROM UserInfo WHERE uname = %s", (uname,))
    user = mysql_cursor.fetchall()
    
    return user

def add_new_user(content):

    uname = content["uname"]
    password = content["password"]

    mysql_cursor.execute("INSERT into UserInfo values (%s, %s, %s, %s)", (
        
        content["name"], 
        content["email"], 
        content["phone"], 
        content["uname"]
        )
    )

    mysql_connector.commit()

    mysql_cursor.execute("INSERT INTO Password VALUES (%s, %s)", (

        uname, 
        support.get_salted_password_hash(uname, password)
        )
    )

    mysql_connector.commit()


def delete_user(uname):

    mysql_cursor.execute("DELETE FROM Token WHERE uname = %s", uname)
    mysql_cursor.execute("DELETE FROM Password WHERE uname = %s", uname)
    mysql_cursor.execute("DELETE FROM UserInfo WHERE uname = %s", uname)
    return not check_if_account_exists(uname)

def update_user_info(uname, user_object):
    pass

def update_user_password():
    pass

def get_user_info():
    pass




###### Authentication ###########################################################

# basic password check

def check_password(uname, password):

    password_hash = support.get_salted_password_hash(uname, password)
    mysql_cursor.execute("SELECT password FROM Password WHERE uname = %s", (uname,))
    password_from_database = mysql_cursor.fetchone()[0]

    if password_hash == password_from_database:
        return True
    else:
        return False

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

    uname = redis_client.get(token)

    if uname: 
        
        redis_client.expire(token, timedelta(minutes=10))
        return uname

    else:
        mysql_cursor.execute("SELECT uname FROM Token WHERE token = %s;", (token,))
        uname = mysql_cursor.fetchall()[0][0]

        if uname: 
            redis_client.expire(token, timedelta(minutes=10))
            return uname

        else: 
            return None

# check password and grant a new user token
def process_login(content):

    uname = content['uname']
    password = content['password']

    if check_password(uname, password):

        return generate_token(uname)