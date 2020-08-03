import os


class DevConfig():
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set unbuffered output, i.e., output is sent immediately to STDOUT instead
    # of being buffered
    os.environ['PYTHONUNBUFFERED'] = "TRUE"

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cash_MapS_Key_Babyy'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/cashmaps/static/resources/database.db')

    #Turns off notifications when the database is updated
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


    UPLOAD_FOLDER_TEMP=os.path.join(basedir +  "/cashmaps/static/resources/temp/")
    UPLOAD_FOLDER_PHOTOS=os.path.join(basedir + "/cashmaps/static/photos/")
    TASK_TYPE_PARSE='parse'


class TestConfig():
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set unbuffered output, i.e., output is sent immediately to STDOUT instead
    # of being buffered
    os.environ['PYTHONUNBUFFERED'] = "TRUE"

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cash_MapS_Key_Babyy'
   

    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/cashmaps/static/resources/test_db.db')

    #Turns off notifications when the database is updated
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


    UPLOAD_FOLDER_TEMP=os.path.join(basedir +  "/cashmaps/static/resources/temp/")
    UPLOAD_FOLDER_PHOTOS=os.path.join(basedir + "/cashmaps/static/photos/")
    TASK_TYPE_PARSE='parse'

    # The port of the Pytest-Flask live server for Browser testing
    LIVESERVER_PORT = 5000
