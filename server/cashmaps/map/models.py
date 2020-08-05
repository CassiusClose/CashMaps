from cashmaps import db
from cashmaps.models import results_to_arr

#Be careful of ForeignKey case! 'ForeignKey' would become 'foreign_key'. Underscores
#are kept

class Track(db.Model):
    """A database model that stores a track, which is a collection of points"""

    id = db.Column(db.Integer, primary_key=True)

    #The track ID as marked in the file, which means often 1-10. This will be redundant across tracks.
    track_id = db.Column(db.Integer)
    filename = db.Column(db.String(60))

    #Relates this track to its list of points
    points = db.relationship('TrackPoint', cascade="all, delete", backref='track', lazy='dynamic')

    def json(self):
        """
        Returns JSON containing the track's data, including all of its points, to be sent
        to the client.
        """
        points = self.points.order_by(TrackPoint.timestamp)
        data = {
            'id':self.id,
            'points': [p.json() for p in points]
        }
        return data


    def get_all_tracks_as_json():
        """
        Returns a list of all tracks, formatted as JSON.
        """
        tracks = Track.query.all()
        return [t.json() for t in tracks]


class TrackPoint(db.Model):
    """A database model that stores points on a map, in lat & long, that form tracks"""

    id = db.Column(db.Integer, primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, unique=True, index=True)

    #Links this point to its track
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))

    def json(self):
        """
        Returns JSON containing the point's data to be sent to the client.
        """
        return {
            'id': self.id,
            'latitude':self.latitude,
            'longitude':self.longitude,
            'timestamp':self.timestamp,
        }
