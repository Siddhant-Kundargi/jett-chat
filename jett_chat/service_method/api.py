from flask import request, jsonify, abort
from jett_chat.DBfn import account
from jett_chat import app

import jett_chat.errors as errors

@app.route('/api/authkey', methods = ['POST'])
def authorize():

    if (request.is_json):

        return jsonify(account.process_login(request.get_json()))

    else:
        return jsonify(errors.not_json_error)

@app.route('/api/message/send', methods = ['POST'])
def recieve_message():

    content = request.get_json()

    print(content['token'])

    uname = account.check_token(content['token'])

    if uname:
        print(uname, content['message'])
        return "200"

    else:
        print(content['token'], "token verification failed...")
        abort(401)