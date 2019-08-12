from app import app
from flask import jsonify

@app.route('/_get_data', methods=['POST'])
def get_data():
    """Passes track data along to the Cesium widget to be displayed"""

    point_data = data_compiler.get_track_data()
    return jsonify(point_data)
