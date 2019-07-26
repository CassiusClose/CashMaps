from app import db

class Track(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    seg_id = db.Column(db.Integer)
    
class Track_Segment(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)


class Track_Point(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    time = db.Column(db.DateTime, index=True)
