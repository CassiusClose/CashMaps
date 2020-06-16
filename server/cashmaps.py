import eventlet
eventlet.monkey_patch()

from app import app, db, socketio
from app.uploader.models import Photo
from app.map.models import Track, TrackPoint
import logging
import os

#Set logging to info level and disables the prefix to each message
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(message)s')

@app.shell_context_processor
def make_shell_context():
    """Sets up automatic imports for the flask python shell to make testing easier"""

    return {'db':db, 'Track':Track, 'TrackPoint':TrackPoint, 'Photo':Photo}


if __name__ == '__main__':
    socketio.run(app)
