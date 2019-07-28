from app import db

#Be careful of ForeignKey case! 'ForeignKey' would become 'foreign_key'. Underscores
#are kept

class Track(db.Model):
    """A database model that stores a track, which is a collection of points"""

    database_id = db.Column(db.Integer, primary_key=True)

    track_id = db.Column(db.Integer)

    #Relates this track to its list of points
    points = db.relationship('TrackPoint', backref='track', lazy='dynamic')

class TrackPoint(db.Model):
    """A database model that stores points on a map, lat long, that make up tracks"""

    database_id = db.Column(db.Integer, primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, unique=True, index=True)

    #Links this point to its track
    track_id = db.Column(db.Integer, db.ForeignKey('track.database_id'))
