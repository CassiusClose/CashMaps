import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from rq import Queue
from rq.job import Job
from redis import Redis
from flask_socketio import SocketIO

#templates: templates, static: template/dist/

db = SQLAlchemy()
migrate = Migrate()
redis = Redis.from_url(os.environ.get('REDIS_URL') or 'redis://')
queue = Queue('cashmaps', connection=redis)
socketio = SocketIO()


def create_app(ConfigClass):
    app = Flask(__name__, template_folder='', static_folder='static/')
    app.config.from_object(ConfigClass)
    app.debug = True



    #TEMPORARY, hides standard GET and POST requests to declutter the term for finding errors
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)


    #Databasing and migration of changes
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)


        if app.config.get('TESTING'):
            socketio.init_app(app)
        else:
            socketio.init_app(app, message_queue=app.config['REDIS_URL'])
        

        from cashmaps.parsing import parsing_bp
        app.register_blueprint(parsing_bp)

        from cashmaps.map import map_bp
        app.register_blueprint(map_bp)

        from cashmaps.uploader import uploader_bp
        app.register_blueprint(uploader_bp)

        from cashmaps import routes, models


        return app
