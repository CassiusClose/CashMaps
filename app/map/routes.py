from app.map import map_bp
from app.map.models import Track, TrackPoint
from flask import jsonify

@map_bp.route('/map/_get_data', methods=['POST'])
def map_get_data():
    """Passes track data along to the Cesium widget to be displayed"""
    return Track.get_tracks()
