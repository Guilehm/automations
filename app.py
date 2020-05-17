import os

from flask import Flask

app = Flask(__name__)

DEBUG = os.getenv('DEBUG', True)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)
