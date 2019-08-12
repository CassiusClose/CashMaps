from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from rq import Queue
from rq.job import Job
from redis import Redis

#templates: templates, static: template/dist/

app = Flask(__name__, template_folder='templates', static_folder='templates/dist/')
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

redis = Redis.from_url(app.config['REDIS_URL'])
queue = Queue('cashmaps', connection=redis)


from app.parsing import parsing_bp
app.register_blueprint(parsing_bp)



from app import routes, models
