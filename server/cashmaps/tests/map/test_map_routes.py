import datetime
import json

from cashmaps.map.models import *
from cashmaps.tests.fixtures import app, worker, browser, database

class TestPostCalls:
    """
    Tests map-related POST routes that let the client perform certain tasks.
    """

    def test_clear_tracks(self, app, database):
        """
        '/map/_clear_data' should delete all tracks from the database.
        """
        client = app.test_client()

        t = Track(track_id=1, filename='file')
        t1 = Track(track_id=1, filename='file')
        p1 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(2019,1,1,1,1,1), track=t)
        p2 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(2019,1,1,1,1,2), track=t)
        p3 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(2019,1,1,1,1,3), track=t1)
        db.session.add_all([t, t1, p1, p2, p3])
        db.session.commit()

        client.delete('/map/_clear_data')

        assert Track.query.count() == 0
        assert TrackPoint.query.count() == 0


    def test_get_map_data(self, app, database):
        """
        '/map/_get_data' should return JSON containing the data of all tracks.
        """
        client = app.test_client()

        t = Track(track_id=1, filename='file')
        t1 = Track(track_id=1, filename='file')
        p1 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(2019,1,1,1,1,1), track=t)
        p2 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(2019,1,1,1,1,2), track=t)
        p3 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(2019,1,1,1,1,3), track=t1)
        db.session.add_all([t, t1, p1, p2, p3])
        db.session.commit()

        results = client.get('/map/_get_data')

        dictionary = {'tracks': Track.get_all_tracks_as_json()}
        for t in dictionary['tracks']:
            for p in t['points']:
                p['timestamp'] = p['timestamp'].strftime("%a, %d %b %Y %I:%M:%S GMT")

        print(dictionary)
        print(json.loads(results.data))

        assert json.loads(results.data.decode()) == dictionary
