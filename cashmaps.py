from app import app, db
from app.models import Track, TrackSegment, TrackPoint

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Track':Track, 'TrackSegment':TrackSegment, 'TrackPoint':TrackPoint}
