import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cash_MapS_Key_Babyy'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + 'app/static/resources/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

