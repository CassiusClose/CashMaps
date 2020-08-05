import os

class BaseConfig():
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set unbuffered output, i.e., output is sent immediately to STDOUT instead
    # of being buffered
    os.environ['PYTHONUNBUFFERED'] = "TRUE"

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cash_MapS_Key_Babyy'

    #Turns off notifications when the database is updated
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis server for running background tasks
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    # Where are uploaded files stored
    UPLOAD_FOLDER_TEMP=os.path.join(basedir +  "/cashmaps/static/resources/temp/")
    UPLOAD_FOLDER_PHOTOS=os.path.join(basedir + "/cashmaps/static/photos/")

    # Socket namespaces
    TASK_TYPE_PARSE = 'parse'


class DevConfig(BaseConfig):

    # Set unbuffered output, i.e., output is sent immediately to STDOUT instead
    # of being buffered
    os.environ['PYTHONUNBUFFERED'] = "TRUE"

    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.basedir + '/cashmaps/static/resources/database.db')


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseConfig.basedir + '/cashmaps/static/resources/test_db.db')


    # The port of the Pytest-Flask live server for Browser testing
    LIVESERVER_PORT = 5000
