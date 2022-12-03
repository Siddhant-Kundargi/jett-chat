from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

import jett_chat.service_method.api
import jett_chat.service_method.web_app