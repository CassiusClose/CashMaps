import pathlib
import pytest
import datetime
import os

from werkzeug.datastructures import FileStorage

#from cashmaps import db
from cashmaps.map.models import *
from cashmaps.tasks import start_task
from cashmaps.tests.fixtures import app, worker, database, socketio_client
from cashmaps.tests.parsing.utils import get_testfile_path
from cashmaps.parsing.parsers.homeport_parser import parse_homeport
from cashmaps.parsing.routes import start_parse



class TestHomeportParser:
    """
    Tests that the Homeport parser will parse homeport files correctly. Tests a variety
    of success cases.
    """

    def test_standard_parse(self, app, database):
        """
        Test that parse_homeport will properly parse a well-formatted file exported from
        Garmin Homeport, and will create the proper amount of Tracks and Track Points that
        are linked together.
        """
        filepath = get_testfile_path('standard.txt')

        parse_homeport(filepath)

        assert Track.query.count() == 10
        assert TrackPoint.query.count() == 100
        for t in Track.query.all():
            assert t.points.count() == 10

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

        for i in range(0, Track.query.count()):
            t = Track.query[i]
            assert t.points[0].timestamp == timestamps[i]
            assert t.points[0].latitude == lats[i]
            assert t.points[0].longitude == longs[i]


    def test_same_points(self, app, database):
        """
        Test that parse_homeport() will not create multiple identical points, i.e. will
        skip any duplicate points.
        """
        filepath = get_testfile_path('duplicate_points.txt')
        parse_homeport(filepath)

        assert Track.query.count() == 1
        assert TrackPoint.query.count() == 1


    def test_empty_parse(self, app, database):
        """
        Test that parse_homeport(), when given a file with no listed tracks or track points,
        will not fail and will not create any database models.
        """
        filepath = get_testfile_path('empty_data.txt')
        parse_homeport(filepath)

        assert Track.query.count() == 0
        assert TrackPoint.query.count() == 0


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
        assert Track.query[0].points.order_by(TrackPoint.id.desc()).first().timestamp == time2
    

class TestHomeportParserAsTask:
    """
    Tests the parser when pushed as a job to the Redis Queue as a background task. This
    tests that callbacks from that job are called, which do cleanup tasks like deleting
    the parsed file from the temp directory. This class tests a whole bunch of different
    cases where parsing would fail, and tests that the error callback is called as well.

    It also tests that socket messages are sent properly, which currently will only happen
    when the parse is done as a RQ Job.
    """

    def test_parse_task_fine(self, app, socketio_client, database, worker):
        """
        Tests that a successful parse creates the proper database objects, and removes
        the parsed file from the temp directory.

        Also tests that the proper socket messages were sent: one signaling the start
        of the parse, one signaling the successful completion of the parse, and many
        updating the job's progress in the middle.
        """
        # Open the file to be parsed
        parse_filename = 'standard.txt'
        filepath = get_testfile_path(parse_filename)
        f = open(filepath, 'rb')
        #file = FileStorage(filename=filepath) #simulate post request file object
        file = FileStorage(stream=f)

        # Connect to the socket
        socketio_client.connect(namespace='/parsers')

        # Do the parse
        job = start_parse(file)
        worker.work(burst=True)

        # No database objects should have been created
        assert Track.query.count() == 10
        assert TrackPoint.query.count() == 100

        # The temp file should be gone, and it shouldn't change the original one.
        assert not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER_TEMP'],parse_filename))
        assert os.path.exists(filepath)

        # Get all socket messages that were sent
        received_messages = socketio_client.get_received(namespace='/parsers')

        # Ensure the message from the parser beginning was sent
        assert received_messages[0]['name'] == 'parser_start'
        assert received_messages[0]['args'][0]['job_id'] == job.id
        assert received_messages[0]['args'][0]['filename'] == parse_filename

        # Ensure the message from the parser finishing was sent 
        assert received_messages[-1]['name'] == 'parser_finish'
        assert received_messages[-1]['args'][0]['job_id'] == job.id
        assert received_messages[-1]['args'][0]['filename'] == parse_filename

        # Ensure the progress messages were sent
        for i in range(1, len(received_messages)-2):
            m = received_messages[i]
            assert m['name'] == 'parser_update'
            assert m['args'][0]['job_id'] == job.id
            assert m['args'][0]['filename'] == parse_filename
            assert m['args'][0]['max_progress'] == 100
            assert m['args'][0]['progress'] == i-1


    def _test_parse_task_error(self, app, socketio_client, database, worker, filename):
        """
        A helper function. Called by the following tests.
        Tests that parsing the given file will result in error, i.e. not saving any
        data to the database, but still removing the parsed file from the temp directory.

        Also tests that the proper socket messages were sent: One signaling the beginning
        of the parsing, many updates of the job's progress, and one signaling that the
        parse failed.
        """
        # Load the file to be parsed in a file object
        filepath = get_testfile_path(filename)
        f = open(filepath, 'rb')
        file = FileStorage(stream=f) #simulate post request file object

        # Connect to the socket
        socketio_client.connect(namespace='/parsers')

        # Do the parse
        job = start_parse(file)
        worker.work(burst=True)

        # No database objects should have been created
        assert Track.query.count() == 0
        assert TrackPoint.query.count() == 0

        # The temp file should be gone, and it shouldn't change the original one.
        assert not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER_TEMP'],filename))
        assert os.path.exists(filepath)
        

        # Get all socket messages that were sent
        received_messages = socketio_client.get_received(namespace='/parsers')

        # Ensure the parser start message was sent
        assert received_messages[0]['name'] == 'parser_start'
        assert received_messages[0]['args'][0]['job_id'] == job.id
        assert received_messages[0]['args'][0]['filename'] == filename 

        # Ensure the parser failure message was sent
        assert received_messages[-1]['name'] == 'parser_error'
        assert received_messages[-1]['args'][0]['job_id'] == job.id
        assert received_messages[-1]['args'][0]['filename'] == filename 

        # Ensure the parser progerss messages were sent
        for i in range(1, len(received_messages)-2):
            m = received_messages[i]
            assert m['name'] == 'parser_update'
            assert m['args'][0]['job_id'] == job.id
            assert m['args'][0]['filename'] == filename
            assert m['args'][0]['max_progress'] == 100
            assert m['args'][0]['progress'] == i-1


    def test_parse_task_error_file_random_text(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file is just random sentences.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'random_text.txt')


    def test_parse_task_error_empty_file(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file contains no text.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'empty_file.txt')


    def test_parse_task_error_bad_lat_long(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file has an incorrectly
        formatted latitude or longitude point.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'bad_lat_long.txt')


    def test_parse_task_error_bad_track_id(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file has a track id that
        is negative.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'bad_track_id.txt')


    def test_parse_task_error_bad_point_track_id(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file has a point that
        has a track id that doesn't match any track listed in the file.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'bad_point_track_id.txt')


    def test_parse_task_error_bad_timestamp(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file has a timestamp that's
        formatted incorrectly.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'bad_timestamp.txt')


    def test_parse_task_error_bad_tabs(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file doesn't have tabs between
        its pieces of data.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'bad_tabs.txt')


    def test_parse_task_error_missing_sections(self, app, socketio_client, database, worker):
        """
        Tests that the parser fails correctly when the file doesn't have all the
        sections that a homeport parser is supposed to have.
        """
        self._test_parse_task_error(app, socketio_client, database, worker, 'missing_sections.txt')
