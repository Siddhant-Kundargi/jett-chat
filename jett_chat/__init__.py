from jett_chat.DBfn.initialiseDatabase import initialize_database
mysql_connector, mongodb_connector, redis_client = initialize_database()

from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

import jett_chat.service_method.api
import jett_chat.service_method.web_app