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
