import datetime
from hashlib import sha256, sha512
from access_control import get_conversation_id
from jett_chat import mysql_connector, mongodb_connector

# get last message id
# if first message

def get_conversation_queues(conversation_id, reciever):

    queue_collection = mongodb_connector["queue"]
    return queue_collection.find_one({'conversation_id' : conversation_id})[reciever]

def push_to_queue(conversation_id, message_id, reciever):

    queue_collection = mongodb_connector["queue"]

    old_list = get_conversation_queues(conversation_id, reciever)
    new_list = old_list.append(message_id)

    selector_query = {"conversation_id": conversation_id}
    setter_query = { "$set": { reciever: new_list }}

    queue_collection.update_one(selector_query, setter_query)
    return 1

def push_message(message, sender, reciever):

    conversation_id = get_conversation_id()

    message_id = get_last_message_id(conversation_id) + 1
    conversation_collection = mongodb_connector[conversation_id]

    message_document = {"messageid" : message_id, "sender" : sender, "date" : datetime.datetime.now(), "message" : message}
    conversation_collection.insert_one(message_document)

    push_to_queue(conversation_id, message_id, reciever)

    return 1

def process_first_message(message, sender, reciever):

    conversation_id = sha512(sha256(sender.encode('utf-8')).hexdigest().encode('utf-8') + sha256(reciever.encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()[:61]

    message_id = 1

    mycursor.execute('INSERT INTO Conversation values(%s,%s,%s)', (sender, reciever, conversation_id,))

    queue_collection = mongodb_connector["queue"]

    queue_data = {'conversation_id': conversation_id, sender: [], reciever: [message_id]}
    queue_collection.insert_one(queue_data)

    conversation_collection = mongodb_connector[conversation_id]

    message_document = {"messageid" : message_id, "sender" : sender, "date" : datetime.datetime.now(), "message" : message}
    conversation_collection.insert_one(message_document)

def get_new_messages(username):
    pass