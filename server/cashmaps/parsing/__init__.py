from flask import Blueprint

parsing_bp = Blueprint('parsing', __name__)

from cashmaps.parsing import routes
