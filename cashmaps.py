from app import app, db
from app.models import Track, TrackPoint
import logging
import os

#Set logging to info level and disables the prefix to each message
#logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%s(message)s')

@app.shell_context_processor
def make_shell_context():
    """Sets up automatic imports for the flask python shell to make testing easier"""

    return {'db':db, 'Track':Track, 'TrackPoint':TrackPoint}
