from werkzeug.datastructures import FileStorage

from cashmaps import queue
from cashmaps.tests.fixtures import app, worker, browser
from cashmaps.tests.parsing.utils import get_testfile_path

class TestPostCalls:
    """
    Tests misc POST routes that let the client perform certain tasks.
    """

    def test_start_parse(self, app, client):
        """
        '/_rq_clear' clears the Redis Queue, used to clear up stale RQ jobs generated
        in developments.
        """
        queue.empty()
        #client = app.test_client()

        f1path = get_testfile_path('standard.txt')
        f1 = open(f1path, 'rb')
        file1 = FileStorage(stream=f1)

        f2path = get_testfile_path('standard.txt')
        f2 = open(f2path, 'rb')
        file2 = FileStorage(stream=f2)

        data = {
            'files': [f1, f2]
        }

        client.post('/parser/_start_parse', data={'0': f1, '1': f2})

        assert len(queue.jobs) == 2
        queue.empty()

