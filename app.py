import os

from flask import Flask

app = Flask(__name__)

DEBUG = os.getenv('DEBUG', True)
PORT = os.getenv('PORT', 5000)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
