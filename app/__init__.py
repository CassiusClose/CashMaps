from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#templates: templates, static: template/dist/
app = Flask(__name__, static_folder='templates/dist/', template_folder='templates')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
