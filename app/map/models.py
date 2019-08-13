from app import db

#Be careful of ForeignKey case! 'ForeignKey' would become 'foreign_key'. Underscores
#are kept

class Track(db.Model):
    """A database model that stores a track, which is a collection of points"""

    database_id = db.Column(db.Integer, primary_key=True)

    track_id = db.Column(db.Integer)

    #Relates this track to its list of points
    points = db.relationship('TrackPoint', backref='track', lazy='dynamic')

    def to_dict(self):
        points = self.points.order_by(TrackPoint.timestamp)
        data = {'database_id':self.database_id, 'track_id':self.track_id, 'points':Track.results_to_arr(points)}
        return data

    def get_tracks():
        tracks = Track.query.all()
        return {'tracks': Track.results_to_arr(tracks)}

    def results_to_arr(results):
        arr = []
        for obj in results:
            arr.append(obj.to_dict())
        return arr

class TrackPoint(db.Model):
    """A database model that stores points on a map, lat long, that make up tracks"""

    database_id = db.Column(db.Integer, primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, unique=True, index=True)

    #Links this point to its track
    track_id = db.Column(db.Integer, db.ForeignKey('track.database_id'))

    def to_dict(self):
         return {'latitude':self.latitude, 'longitude':self.longitude, 'timestamp':self.timestamp, 'track_id':self.track_id}
