from jett_chat import mysql_connector, mongodb_connector

def get_conversation_id(uname1, uname2):

    mysql_cursor = mysql_connector.cursor()

    mysql_cursor.execute("SELECT conversationId FROM Conversation WHERE uname1 = %s AND uname2 = %s", (uname1,uname2))

    try:
        return mysql_cursor.fetchall()[0][0]
    except:
        return None