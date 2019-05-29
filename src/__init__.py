import asyncio

import base64
import time

from flask import Flask
from flask_socketio import SocketIO



app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet", async_handlers=True)

from src import routes
from src import socket