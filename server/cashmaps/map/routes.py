from cashmaps.map import map_bp
from cashmaps.map.models import Track, TrackPoint
from flask import jsonify, current_app

@map_bp.route('/map/_get_data', methods=['POST'])
def map_get_data():
    """Returns track data for the Cesium widget to display"""
    return Track.get_tracks()

@map_bp.route('/map/_clear_data', methods=['POST'])
def map_clear_data():
    Track.clear_tracks()
    FlashMessage.create_message("Tracks Cleared", current_app.config['TASK_TYPE_MAP'])
    return {}
