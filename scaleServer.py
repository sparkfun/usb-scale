#! /usr/bin/env python

# This will run as a production ready server if something like eventlet is installed

import json
import threading

from readscale import USBScale

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = 0
scale = USBScale()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def send_weight(weight, reschedule=0.1):
    """
    broadcast the weight on the scale to listeners
    :param weight: dictionary with
    :param reschedule: time delay to reschedule the function
    :return: None
    """
    socketio.send(
        json.dumps(weight, json=True)
    )
    if reschedule:
        threading.Timer(reschedule, send_weight)


@socketio.on('connect')
def serve_weight():
    global clients
    socketio.send('Connected')
    dummy_weight = {'lbs': 1,
                    'oz': 15.6}
    clients += 1
    while clients:
        socketio.send(
            json.dumps(dummy_weight, json=True)
        )


@socketio.on('disconnect')
def disconnect():
    global clients
    clients -= 1


if __name__ == '__main__':
    # Default here is 127.0.0.1 and port 5000
    socketio.run(app)
