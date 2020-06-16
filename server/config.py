import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set unbuffered output, i.e., output is sent immediately to STDOUT instead
    # of being buffered
    os.environ['PYTHONUNBUFFERED'] = "TRUE"

    #For encryption or something
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cash_MapS_Key_Babyy'

    #Database location
    #sqlite: followed by 4 slashes is absolute, 3 is relative
    #Using absolute was how I got it to work, but that's okay because basedir is
    #determined at the beginning
    #Preferably, it could just be done from the static location
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        #'sqlite:////' + os.path.join(basedir +  '/app/static/resources/database.db')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/app/static/resources/database.db'
    #Turns off notifications when the database is updated
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


    UPLOAD_FOLDER_TEMP=os.path.join(basedir +  "/app/static/resources/temp/")
    UPLOAD_FOLDER_PHOTOS=os.path.join(basedir + "/app/static/photos/")



    TASK_TYPE_PARSE = "parse"
    TASK_TYPE_MAP = "map"
    FLASH_TYPE_UPLOAD = "upload_flash"