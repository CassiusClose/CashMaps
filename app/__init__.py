from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from rq import Queue
from rq.job import Job
from redis import Redis

#templates: templates, static: template/dist/

app = Flask(__name__, template_folder='', static_folder='static/')
app.config.from_object(Config)
app.debug = True


#TEMPORARY, hides standard GET and POST requests to declutter the term for finding errors
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)


#Databasing and migration of changes
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#For scheduling background tasks
redis = Redis.from_url(app.config['REDIS_URL'])
queue = Queue('cashmaps', connection=redis)


from app.parsing import parsing_bp
app.register_blueprint(parsing_bp)

from app.map import map_bp
app.register_blueprint(map_bp)

from app.uploader import uploader_bp
app.register_blueprint(uploader_bp)


from app import routes, models
