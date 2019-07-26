from app import db

class Track(db.Model):
    databaseId = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer)
    segments = db.relationship('TrackSegment', backref='track', lazy='dynamic')
    
class TrackSegment(db.Model):
    databaseId = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer)
    points = db.relationship('TrackPoint', backref='segment', lazy='dynamic')
    trackId = db.Column(db.Integer, db.ForeignKey('track.track_id'))

class TrackPoint(db.Model):
    databaseId = db.Column(db.Integer, primary_key=True)
    pointId = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True)
    segmentId = db.Column(db.Integer, db.ForeignKey('track_segment.segment_id'))
