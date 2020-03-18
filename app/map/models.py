from app import db
from app.models import results_to_arr

#Be careful of ForeignKey case! 'ForeignKey' would become 'foreign_key'. Underscores
#are kept

class Track(db.Model):
    """A database model that stores a track, which is a collection of points"""

    database_id = db.Column(db.Integer, primary_key=True)

    #The track ID as marked in the file, which means often 1-10. This will be redundant across tracks.
    track_id = db.Column(db.Integer)

    #Relates this track to its list of points
    points = db.relationship('TrackPoint', backref='track', lazy='dynamic')

    def to_dict(self):
        """Returns a dictionary representation of this object to be used as JSON."""
        points = self.points.order_by(TrackPoint.timestamp)
        data = {'database_id':self.database_id, 'track_id':self.track_id, 'points':results_to_arr(points)}
        return data

    def get_tracks():
        """Returns all the tracks as a dictionary, to be sent as JSON."""
        tracks = Track.query.all()
        return {'tracks': results_to_arr(tracks)}

class TrackPoint(db.Model):
    """A database model that stores points on a map, in lat & long, that form tracks"""

    database_id = db.Column(db.Integer, primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, unique=True, index=True)

    #Links this point to its track
    track_id = db.Column(db.Integer, db.ForeignKey('track.database_id'))

    def to_dict(self):
        """Returns a dictionary representation of this object to be used as JSON."""
        return {'latitude':self.latitude, 'longitude':self.longitude, 'timestamp':self.timestamp, 'track_id':self.track_id}
