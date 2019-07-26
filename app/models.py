from app import db

class Track(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer)
    segments = db.relationship('Segment', backref='track', lazy='dynamic')
    
class Track_Segment(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer)
    points = db.relationship('Point', backref='segment', lazy='dynamic')

class Track_Point(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True)
