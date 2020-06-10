import os

basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['PYTHONUNBUFFERED'] = "TRUE"

class Config(object):
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
    print(SQLALCHEMY_DATABASE_URI)
    #Turns off notifications when the database is updated
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:5000/0'


    UPLOAD_FOLDER_TEMP=os.path.join(basedir +  "/app/static/resources/temp/")
    UPLOAD_FOLDER_PHOTOS=os.path.join(basedir + "/app/static/photos/")



    TASK_TYPE_PARSE = "parse"
    TASK_TYPE_MAP = "map"
    FLASH_TYPE_UPLOAD = "upload_flash"
