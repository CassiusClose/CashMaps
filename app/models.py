from app import db

#Be careful of ForeignKey case! 'ForeignKey' would become 'foreign_key'. Underscores
#are kept

class Track(db.Model):
    """A database model that stores a track, which is a collection of points"""

    database_id = db.Column(db.Integer, primary_key=True)

    track_id = db.Column(db.Integer, unique=True)

    #Relates this track to its list of points
    points = db.relationship('TrackPoint', backref='track', lazy='dynamic')

class TrackPoint(db.Model):
    """A database model that stores points on a map, lat long, that make up tracks"""

    #A multi-column uniqueness constraint, makes sure no TrackPoint can have the same
    #point_id and track_id
    #__table_args_ must be a tuple, so include that comma
    __table_args__ = (db.UniqueConstraint('point_id', 'track_id'),)

    database_id = db.Column(db.Integer, primary_key=True)

    point_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True)

    #Links this point to its track
    track_id = db.Column(db.Integer, db.ForeignKey('track.track_id'))
