def initialize_database():
    
    import mysql.connector
    import pymongo
    import redis

    import config

    mongodb_client = pymongo.MongoClient('mongodb://localhost:27017') #, username="mongoadmin", password="password12123")

    mongodb_connector = mongodb_client["jc"]

    mysql_connector = mysql.connector.connect(
        host = "localhost",
        user = config.mysql_user,
        password = config.mysql_password
    )

    mycursor = mysql_connector.cursor()

    mycursor.execute("SHOW DATABASES")
    list_of_databases = mycursor.fetchall()

    if not ('user',) in list_of_databases:

        print("[!!] database not found, creating one")

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
                password varchar(64),
                PRIMARY KEY (uname), 
                FOREIGN KEY (uname) REFERENCES UserInfo(uname))
                """)
        mycursor.execute("""CREATE TABLE Conversation(uname1 varchar(30), 
                uname2 varchar(30), 
                conversationId varchar(60),
                PRIMARY KEY(conversationId))
                """)
        
        print("[+] Database Created")

    else:
        print("[*] Database Already Exists")


    mysql_connector.database = "user"

    return mysql_connector, mongodb_connector, redis.Redis()