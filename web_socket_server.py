from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
app = Flask(__name__)

class WebSocketServer:
    def __init__(self, debug=True):
        self.create_app(app)

    def create_app(self, debug=False):
        app.debug = debug
        socketio.init_app(app, cors_allowed_origin="*")
        return app