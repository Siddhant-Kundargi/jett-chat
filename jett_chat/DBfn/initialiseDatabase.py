def initialize_database():
    
    import mysql.connector
    import pymongo
    import redis

    mongodb_connector = pymongo.MongoClient('')

    mysql_connector = mysql.connector.connect(
        host="localhost",
        user="root",   #creds.username,
        password="@root123"   #creds.password
    )

    mycursor = mysql_connector.cursor()

    mycursor.execute("SHOW DATABASES")
    list_of_databases = mycursor.fetchall()

    if not ('user',) in list_of_databases:

        print("database not found, creating one")

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
        mycursor.execute("""CREATE TABLE Conversation(uname1 varchar(30), 
                uname2 varchar(30), 
                conversationId varchar(60),
                PRIMARY KEY(conversationId))
                """)
        
        print("Database Created")

    else:
        print("Database Already Exists")


    return mysql_connector, mongodb_connector, redis.Redis()

initialize_database()