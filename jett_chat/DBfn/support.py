from hashlib import sha256
import mysql.connector

def get_myql_connectors():

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password123",
        database = "user"
    )
    
    return mydb, mydb.cursor

def get_salted_password_hash(uname, base_password):
    
    # salting done with the username

    base_password_hash = sha256(base_password.encode()).hexdigest()
    salted_hash = sha256((uname + base_password_hash).encode()).hexdigest()

    return salted_hash