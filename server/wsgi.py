import eventlet
eventlet.monkey_patch()

from cashmaps import db, socketio, create_app
from cashmaps.uploader.models import Photo
from cashmaps.map.models import Track, TrackPoint
from config import DevConfig
from flask import current_app
import logging
import os

#Set logging to info level and disables the prefix to each message
#logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(message)s')

app = create_app(DevConfig)

if __name__ == '__main__':
    socketio.run(app)
