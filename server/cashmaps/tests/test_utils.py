import os
from cashmaps.utils import remove_temp_files
from cashmaps.tests.fixtures import app

class TestUtils:
    def test_remove_temp_files(self, app):
        dir = app.config['UPLOAD_FOLDER_TEMP']
        f1 = open(os.path.join(dir, 'test1.txt'), 'w')
        f1.write("Hello. test 1")
        f1.close()
        f2 = open(os.path.join(dir, 'test2.txt'), 'w')
        f2.write("Hello. test 2")
        f2.close()

        remove_temp_files()
        assert len(os.listdir(dir)) == 0
        

