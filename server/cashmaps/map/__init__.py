from flask import Blueprint

map_bp = Blueprint('map', __name__)

from cashmaps.map import routes
