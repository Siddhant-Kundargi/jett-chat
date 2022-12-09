from flask import render_template, abort, request, jsonify
from jett_chat.DBfn import account
from jett_chat.messaging import broker
from jett_chat import app

import jett_chat.errors as errors

@app.route('/')
def hello():
    abort(418)


@app.route('/register', methods = ['GET', 'POST'])
def register_new_user():

    if request.method == 'POST':
        if request.is_json:

            content = request.get_json()

            if not account.check_if_account_exists(content['uname']):
                
                account.add_new_user(content)
                return "User Created"

            else: 

                return jsonify(
                    {
                        "error": "user_already_exists"
                    }
                )
        
        else: 

            return jsonify(errors.not_json_error)
            
    else:
        return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        if (request.is_json):

            return jsonify(account.process_login(request.get_json()))

        else:
            return jsonify(errors.not_json_error)

    else:
        return render_template("login.html")

@app.route('/home', methods = ['GET', 'POST'])
def message_broker():
    
    if request.method == 'POST':
        content = request.get_json()

        if content['content']['token']:

            token = content['content']['token']

            if content['requestPurpose'] == "messageSend":
                uname = account.check_token(token)

                if uname:

                    message = content['content']['messageList'][0]['message']
                    sender = uname
                    reciever = content['content']['messageList'][0]['reciever']
                    broker.push_message(message, sender, reciever)
                    return "200"

                else:
                    abort(401)

            if content['requestPurpose'] == "messageRecieve":

                uname = account.check_token(token)
                sender = content['sender']

                if uname:
                    
                    print(sender, uname)
                    conversation_id = broker.get_conversation_id(sender, uname) 
                    message_list = broker.get_new_messages(conversation_id ,uname)
                    return jsonify({"messageList": list(message_list)})

                else:
                    abort(401)

            if content['requestPurpose'] == "getContactList":

                uname = account.check_token(token)

                if uname:
                    return jsonify({"contactList": broker.get_conversations_list(uname)})
                
                else:
                    abort(401)

        else:
            return "401"

    else:
        
        return render_template("home.html")