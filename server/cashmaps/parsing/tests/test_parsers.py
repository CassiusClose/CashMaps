import pathlib
import pytest
import datetime
import os

from werkzeug.datastructures import FileStorage

#from cashmaps import db
from cashmaps.map.models import *
from cashmaps.tests.fixtures import app, worker, database
from cashmaps.parsing.parsers.homeport_parser import parse_homeport
from cashmaps.parsing.routes import start_parse


def get_testfile_path(filename):
    return pathlib.Path(__file__).parent.absolute() / 'testfiles' / filename


class TestHomeportParser:
    def test_standard_parse(self, app, database):
        """
        Test that parse_homeport will properly parse a well-formatted file exported from
        Garmin Homeport, and will create the proper amount of Tracks and Track Points that
        are linked together.
        """
        filepath = get_testfile_path('standard.txt')


        parse_homeport(filepath)
        

        assert len(Track.query.all()) == 10
        assert len(TrackPoint.query.all()) == 100
        for t in Track.query.all():
            assert len(t.points.all()) == 10

        timestamps = [
            datetime.datetime(2014,8,12,12,54,11),
            datetime.datetime(2014,8,12,12,55,49),
            datetime.datetime(2014,8,12,12,57,28),
            datetime.datetime(2014,8,12,12,59,12),
            datetime.datetime(2014,8,12,13,1,0),
            datetime.datetime(2014,8,12,13,2,49),
            datetime.datetime(2014,8,12,13,4,37),
            datetime.datetime(2014,8,12,13,6,12),
            datetime.datetime(2014,8,12,13,7,43),
            datetime.datetime(2014,8,12,13,9,23),
        ]

        lats = [
            23.613482778891921,
            23.611365174874663,
            23.6090147215873,
            23.606608361005783,
            23.604165622964501,
            23.601644178852439,
            23.599124327301979,
            23.596900859847665,
            23.594782082363963,
            23.592524919658899,
        ]

        longs = [
            -74.844902576878667,
            -74.843598352745175,
            -74.842320363968611,
            -74.840870043262839,
            -74.839416537433863,
            -74.837955487892032,
            -74.836431574076414,
            -74.835062976926565,
            -74.833783144131303,
            -74.832410523667932,
        ]

        for i in range(0, len(Track.query.all())):
            t = Track.query[i]
            assert t.points[0].timestamp == timestamps[i]
            assert t.points[0].latitude == lats[i]
            assert t.points[0].longitude == longs[i]


    def test_empty_parse(self, app, database):
        """
        Test that parse_homeport(), when given a file with no listed tracks or track points,
        will not fail and will not create any database models.
        """
        filepath = get_testfile_path('empty_data.txt')
        parse_homeport(filepath)

        assert len(Track.query.all()) == 0
        assert len(TrackPoint.query.all()) == 0


    def test_empty_tracks_parse(self, app, database):
        """
        Test that parse_homeport(), when given a file where some tracks have no associated
        points, will only create the Track objects that have points associated with them.
        """
        filepath = get_testfile_path('empty_tracks.txt')
        parse_homeport(filepath)

        assert Track.query.count() == 1
        assert Track.query[0].track_id == 1

        time1 = datetime.datetime(2014,8,12,12,54,11)
        time2 = datetime.datetime(2014,8,12,13,10,44)

        assert Track.query[0].points.first().timestamp == time1
        assert Track.query[0].points.order_by(TrackPoint.database_id.desc()).first().timestamp == time2
    

    def _test_parse_task_error(self, app, database, worker, filename):
        filepath = get_testfile_path(filename)
        f = open(filepath)
        file = FileStorage(stream=f) #simulate post request file object

        job = start_parse(file)
        worker.work(burst=True)

        # No database objects should have been created
        assert Track.query.count() == 0
        assert TrackPoint.query.count() == 0

        # The temp file should be gone, and it shouldn't change the original one.
        assert not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER_TEMP'],filename))
        assert os.path.exists(filepath)


    def test_parse_task_error_file_random_text(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'random_text.txt')

    def test_parse_task_error_empty_file(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'empty_file.txt')

    def test_parse_task_error_bad_lat_long(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'bad_lat_long.txt')

    def test_parse_task_error_bad_track_id(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'bad_track_id.txt')

    def test_parse_task_error_bad_point_track_id(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'bad_point_track_id.txt')

    def test_parse_task_error_bad_timestamp(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'bad_timestamp.txt')

    def test_parse_task_error_bad_tabs(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'bad_tabs.txt')

    def test_parse_task_error_missing_sections(self, app, database, worker):
        self._test_parse_task_error(app, database, worker, 'missing_sections.txt')



