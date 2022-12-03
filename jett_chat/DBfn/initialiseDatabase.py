def initialize_database():
    
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",   #creds.username,
        password="password123"   #creds.password
    )

    mycursor = mydb.cursor()

    mycursor.execute("create database user")
    mycursor.execute("use user")
    mycursor.execute("""CREATE TABLE UserInfo(name varchar(50),
            email varchar(40), 
            phone varchar(15), 
            uname varchar(30),
            PRIMARY KEY (uname))
            """)
    mycursor.execute("""CREATE TABLE Token(uname varchar(30), 
            token varchar(160),
            PRIMARY KEY (uname), 
            FOREIGN KEY (uname) REFERENCES UserInfo(uname))
            """)
    mycursor.execute("""CREATE TABLE Password(uname varchar(30),
            password varchar(20),
            PRIMARY KEY (uname), 
            FOREIGN KEY (uname) REFERENCES UserInfo(uname))
            """)

initialize_database()