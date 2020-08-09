from cashmaps import db
from cashmaps.map import map_bp
from cashmaps.map.models import Track, TrackPoint
from flask import jsonify, current_app

@map_bp.route('/map/_get_data', methods=['GET'])
def map_get_data():
    """Returns track data for the Cesium widget to display"""
    tracks = Track.get_all_tracks_as_json()
    return {'tracks': tracks}


@map_bp.route('/map/_clear_data', methods=['DELETE'])
def map_clear_data():
    # Track.query.delete() doesn't cascade properly
    for t in Track.query.all():
        db.session.delete(t)
    db.session.commit()
    return {}
