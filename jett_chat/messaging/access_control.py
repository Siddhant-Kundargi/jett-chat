from jett_chat import mysql_connector, mongodb_connector

def get_conversation_id(uname1, uname2):
    return mysql_connector.execute("SELECT conversationId from conversation WHERE uname1 == %s and uname == %s", (uname1,uname2))[0]