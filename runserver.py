from os import environ
from jett_chat import app

if __name__ == '__main__':
    # HOST = "0.0.0.0"
    # try:
    #     PORT = int(environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    app.run(host='0.0.0.0', port=5555)