#! /usr/bin/env python

# This will run as a production ready server if something like eventlet is installed

import json
import threading

from readscale import set_scale

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode="threading")
# socketio = SocketIO(app)

clients = 0
scale = set_scale()


@app.route('/', methods=['GET'])
def index():
    scale.update()
    return render_template('index.html', lbs=scale.pounds, ozs=scale.ounces)


def send_weight(reschedule=0.2):
    """
    broadcast the weight on the scale to listeners
    :param weight: dictionary with
    :param reschedule: time delay to reschedule the function
    :return: None
    """
    scale.update()
    weight = {
        'lbs': scale.pounds,
        'ozs': scale.ounces
    }
    if clients:
        socketio.send(weight)
    if reschedule and clients:
        threading.Timer(reschedule, send_weight).start()


@socketio.on('connect')
def serve_weight():
    global clients
    clients += 1
    send_weight()


@socketio.on('disconnect')
def disconnect():
    global clients
    clients -= 1


if __name__ == '__main__':
    # Default here is 127.0.0.1 and port 5000
    socketio.run(app)
