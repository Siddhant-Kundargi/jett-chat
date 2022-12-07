import datetime
from hashlib import sha256, sha512
from jett_chat.messaging.access_control import get_conversation_id
from jett_chat import mysql_connector, mongodb_connector
# if first message

def get_last_message_id(conversation_id):

    print("getLastMessageId: 1: ",conversation_id)

    conversation_collection = mongodb_connector[str(conversation_id)]
    last_message_id = conversation_collection.find().sort("messageid", -1)[0]["messageid"]

    return last_message_id


def get_conversation_queues(conversation_id, reciever):

    queue_collection = mongodb_connector["queue"]
    conversation_queue = queue_collection.find_one({'conversation_id' : conversation_id})[reciever]

    return conversation_queue

def push_to_queue(conversation_id, message_id, reciever):

    queue_collection = mongodb_connector["queue"]

    old_list = get_conversation_queues(conversation_id, reciever)

    if not old_list:
        old_list = []

    new_list = old_list.append(message_id)

    selector_query = {"conversation_id": conversation_id}
    setter_query = { "$set": { reciever: new_list }}

    queue_collection.update_one(selector_query, setter_query)

def push_message(message, sender, reciever):

    conversation_id = get_conversation_id(sender, reciever)
    print(conversation_id)

    if conversation_id:

        message_id = get_last_message_id(conversation_id) + 1

    if not conversation_id:

        conversation_id = process_first_message(sender, reciever)
        message_id = 1


    conversation_collection = mongodb_connector[str(conversation_id)]

    message_document = {"messageid" : message_id, "sender" : sender, "date" : datetime.datetime.now(), "message" : message}
    conversation_collection.insert_one(message_document)

    push_to_queue(conversation_id, message_id, reciever)

def process_first_message(sender, reciever):

    mysql_cursor = mysql_connector.cursor()

    senderid_hash_encoded = sha256(sender.encode('utf-8')).hexdigest().encode('utf-8')
    recieverid_hash_encoded = sha256(reciever.encode('utf-8')).hexdigest().encode('utf-8')

    conversation_id = sha512(senderid_hash_encoded + recieverid_hash_encoded).hexdigest()[:60]

    mysql_cursor.execute('INSERT INTO Conversation values(%s,%s,%s)', (sender, reciever, conversation_id,))
    mysql_connector.commit()

    queue_collection = mongodb_connector["queue"]

    queue_data = {'conversation_id': conversation_id, sender: [], reciever: []}
    queue_collection.insert_one(queue_data)

    return conversation_id

def get_new_messages(username):
    pass