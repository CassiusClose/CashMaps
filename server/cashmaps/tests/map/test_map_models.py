import datetime

from cashmaps.map.models import *
from cashmaps.tests.fixtures import app, database

class TestMapModelsCascadeDelete:
    """
    This class tests that the models' cascade delete functionality is setup and working
    properly. In other words, when a "parent" model is deleted, its children will be
    deleted as well.
    """

    def test_trackpoint_deleted_with_track(self, app, database):
        """
        When a Track object is deleted, any associated TrackPoint objects should also be
        deleted.
        """
        t = Track(track_id=1, filename="test_file")
        p1 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,1),
                track=t)
        p2 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,2),
                track=t)
        p3 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,3),
                track=t)
        p4 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,4),
                track=t)
        p5 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,5),
                track=t)
        database.session.add_all([t, p1, p2, p3, p4, p5])
        database.session.commit()

        assert database.session.query(Track).count() == 1
        assert database.session.query(TrackPoint).count() == 5

        database.session.delete(t)
        database.session.commit()

        assert database.session.query(Track).count() == 0
        assert database.session.query(TrackPoint).count() == 0


    def test_track_not_deleted_with_trackpoint(self, app, database):
        """
        When a TrackPoint object is deleted, the associated Track object should not be
        deleted.
        """
        t = Track(track_id=1, filename="test_file")
        p1 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,1),
                track=t)
        p2 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,2),
                track=t)
        p3 = TrackPoint(latitude=1.0, longitude=2.0, timestamp=datetime.datetime(1000,1,3),
                track=t)
        database.session.add_all([t, p1, p2, p3])
        database.session.commit()

        assert database.session.query(Track).count() == 1
        assert database.session.query(TrackPoint).count() == 3

        database.session.delete(p2)
        database.session.commit()

        assert database.session.query(Track).count() == 1
        assert database.session.query(TrackPoint).count() == 2


class TestTrackFunctions:
    """
    Tests the custom functions in the Track database model class.
    """

    def test_track_json(self, app, database):
        """
        Track.json() function should return JSON containing that track's data.
        """
        t = Track(track_id=1, filename="file")
        p1 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 10),
                track=t)
        p2 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 11),
                track=t)
        p3 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 12),
                track=t)
        p4 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 13),
                track=t)
        db.session.add_all([t, p1, p2, p3, p4])
        db.session.commit()

        json = {
            'id': t.id,
            'points': [p1.json(), p2.json(), p3.json(), p4.json()]
        }
        assert t.json() == json


    def test_track_json_no_points(self, app, database):
        """
        Track.json() function should return JSOn containing that track's data,
        even if there are no points associated with that Track.
        """
        t = Track(track_id=1, filename="file")
        db.session.add(t)
        db.session.commit()

        json = {
            'id': t.id,
            'points': []
        }
        assert t.json() == json


    def test_get_all_tracks_as_json(self, app, database):
        """
        get_all_tracks_as_json() should return an array of JSON of every Track in the
        database.
        """
        t1 = Track(track_id=1, filename="file")
        p1 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 10),
                track=t1)
        p2 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 11),
                track=t1)
        p3 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 12),
                track=t1)
        p4 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 13),
                track=t1)
        t2 = Track(track_id=2, filename="file")
        p5 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 14),
                track=t2)
        p6 = TrackPoint(latitude=1.0, longitude=1.0, timestamp=datetime.datetime(10, 10, 15),
                track=t2)
        t3 = Track(track_id=3, filename="file")
        db.session.add_all([t1, t2, t3, p1, p2, p3, p4, p5, p6]) 
        db.session.commit()

        array = [t1.json(), t2.json(), t3.json()]

        assert Track.get_all_tracks_as_json() == array


class TestTrackPointFunctions:
    """
    Tests the custom functions in the TrackPoint database model class.
    """
    
    def test_track_point_json(self, app, database):
        t = Track(track_id=1, filename='test')
        p1 = TrackPoint(latitude=1.15325325023, longitude=-2.5300000006,
                timestamp=datetime.datetime(2019, 3, 20, 20, 5, 36), track=t)
        db.session.add_all([t, p1])
        db.session.commit()

        json = {
            'id': p1.id,
            'latitude': 1.15325325023,
            'longitude': -2.5300000006,
            'timestamp': datetime.datetime(2019, 3, 20, 20, 5, 36)
        }
        assert p1.json() == json
