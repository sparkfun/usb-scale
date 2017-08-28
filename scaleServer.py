#! /usr/bin/env python

# This will run as a production ready server if something like eventlet is installed

import json
import threading
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

from readscale import set_scale


clients = 0
scale = set_scale()


class WeightApp(WebSocketApplication):

    def on_open(self):
        print "Connected!"
        global clients
        if clients:
            clients += 1
            return
        clients += 1
        self.send_weight()

    def on_message(self, message, *args, **kwargs):
        if message:
            print message

    def on_close(self, reason):
        global clients
        clients -= 1
        print reason

    def send_weight(self, reschedule=0.2):
        """
        broadcast the weight on the scale to listeners
        :param weight: dictionary with
        :param reschedule: time delay to reschedule the function
        :return: None
        """
        print 'Sending data...'
        scale.update()
        weight = {
            'lbs': scale.pounds,
            'ozs': scale.ounces
        }
        if clients:
            self.ws.send(json.dumps(weight))
        if reschedule and clients:
            threading.Timer(reschedule, self.send_weight).start()


def static_wsgi_app(environ, start_response):
    """
    Serve a test page
    :param environ:
    :param start_response:
    :return:
    """
    start_response("200 OK", [('Content-Type]', 'text/html')])
    with open("templates/index.html", 'r') as f:
        retval = [bytes(line) for line in f.readlines()]
    return retval


if __name__ == '__main__':
    # Default here is 127.0.0.1 and port 5000
    # socketio.run(app)
    resource = Resource([
        ('/', static_wsgi_app),
        ('/data', WeightApp)
    ])
    WebSocketServer(('localhost', 8000), resource).serve_forever()
