from app import app
from app.map import map_bp
from app.map.models import Track, TrackPoint
from app.models import FlashMessage
from flask import jsonify

@map_bp.route('/map/_get_data', methods=['POST'])
def map_get_data():
    """Returns track data for the Cesium widget to display"""
    return Track.get_tracks()

@map_bp.route('/map/_clear_data', methods=['POST'])
def map_clear_data():
    Track.clear_tracks()
    FlashMessage.create_message("Tracks Cleared", app.config['TASK_TYPE_MAP'])
    return {}

@map_bp.route('/map/_get_flashed_messages', methods=['POST'])
def map_get_flashed_messages():
    return FlashMessage.get_messages_by_type(app.config['TASK_TYPE_MAP'])
