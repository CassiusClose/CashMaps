from app.map import map_bp
from app.map.models import Track, TrackPoint
from flask import jsonify

@map_bp.route('/map/_get_data', methods=['POST'])
def map_get_data():
    """Returns track data for the Cesium widget to display"""
    return Track.get_tracks()
