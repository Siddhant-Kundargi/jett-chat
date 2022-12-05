from flask import render_template, abort, request, jsonify

from jett_chat.DBfn import account
from jett_chat import app
from messaging import broker

import jett_chat.errors as errors

@app.route('/')
def hello():
    print("some stupid checked this site!")
    abort(418)


@app.route('/register', methods = ['GET', 'POST'])
def register_new_user():

    if request.method == 'POST':
        if request.is_json:

            content = request.get_json()

            print(content)

            if not account.check_if_account_exists(content['uname']):
                
                account.add_new_user(content)
                return "User Created"

            else: 

                print("User already exists")
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

        if content['requestPurpose'] == "messageSend":
            print(content['content']['token'])

            uname = account.check_token(content['content']['token'])

            if uname:
                print(uname, content['content']['messageList'][0]['message'])

                return "200"
            else:
                print(content['token'], "token verification failed...")
                abort(401)

        if content['requestPurpose'] == "messageRecieve":

            print(content['token'])

            uname = account.check_token(content)

    else:
        
        return render_template("home.html")