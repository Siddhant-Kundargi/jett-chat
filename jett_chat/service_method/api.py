from flask import request, jsonify, abort
from jett_chat.DBfn import account
from jett_chat import app
from jett_chat.messaging import broker
from jett_chat.messaging import access_control

import jett_chat.errors as errors

@app.route('/api/authkey', methods = ['POST'])
def authorize():

    if (request.is_json):

        return jsonify(account.process_login(request.get_json()))

    else:
        return jsonify(errors.not_json_error)

@app.route('/api/message', methods = ['POST'])
def recieve_message():

    if request.is_json:
        content = request.get_json()

    else:
        return jsonify(errors.not_json_error)

    print(content)

    if content['requestPurpose'] == "messageSend":
        uname = account.check_token(content['content']['token'])

        if uname:

            print(uname, content['content']['messageList'][0]['message'])
            message = content['content']['messageList'][0]['message']
            sender = uname.decode()
            reciever = content['content']['messageList'][0]['reciever']
            broker.push_message(message, sender, reciever)
            return "200"

        else:
            print(content['token'], "token verification failed...")
            abort(401)

    if content['requestPurpose'] == "messageRecieve":

        print(content['token'], content['sender'])
        uname = account.check_token(content['token'])
        sender = content['sender']

        if uname:

            conversation_id = access_control.get_conversation_id(sender, uname) 
            print(conversation_id)
            message_list = broker.get_new_messages(conversation_id ,uname)
            print(message_list)
            return jsonify({"messageList": list(message_list)})

        return "error"