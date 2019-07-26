from app import db

#Be careful of ForeignKey case!
class Track(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer)
    segments = db.relationship('TrackSegment', backref='track', lazy='dynamic')
    
class TrackSegment(db.Model):
    __table_args__ = (db.UniqueConstraint('segment_id', 'track_id'),)
    database_id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer)
    points = db.relationship('TrackPoint', backref='segment', lazy='dynamic')
    track_id = db.Column(db.Integer, db.ForeignKey('track.track_id'))

class TrackPoint(db.Model):
    __table_args__ = (db.UniqueConstraint('point_id', 'segment_id', 'segment.track_id'),)
    database_id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True)
    segment_id = db.Column(db.Integer, db.ForeignKey('track_segment.segment_id'))
