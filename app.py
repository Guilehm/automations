import os
from functools import partial
from threading import Thread

from flask import Flask

from bots.pacino import pacino

app = Flask(__name__)

DEBUG = os.getenv('DEBUG', True)
PORT = os.getenv('PORT', 5000)
DISCORD_PACINO_TOKEN = os.getenv('DISCORD_PACINO_TOKEN')


@app.route('/')
def hello_world():
    return 'Hello, World!'


flask_partial_run = partial(app.run, host='0.0.0.0', port=PORT, debug=DEBUG, use_reloader=False)
flask_thread = Thread(target=flask_partial_run)

if __name__ == '__main__':
    flask_thread.start()
    pacino.run(DISCORD_PACINO_TOKEN)
