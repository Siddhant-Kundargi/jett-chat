def initialize_database():
    
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",   #creds.username,
        password="password123"   #creds.password
    )

    mycursor = mydb.cursor()

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
                unmae2 varchar(30), 
                conversationId varchar(60),
                PRIMARY KEY(conversationId))
                """)
        
        print("Database Created")

    else:
        print("Database Already Exists")

initialize_database()