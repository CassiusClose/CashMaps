from app import app, db
from flask import render_template, jsonify
from app.parsers import homeport_parser
from app.models import Track, TrackPoint

@app.route('/')
@app.route('/index')
def index():
    return render_template('header.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/parser')
def parser():
    homeport_parser.process_file('app/static/resources/track.txt')
    return render_template('header.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    point_data = get_track_data()
    return jsonify(point_data)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def get_track_data():
    data = {}
    for track in Track.query.all():
        track_data = {'id':track.track_id, 'point_count':len(track.points.all())}
        for point in track.points.all():
            point_data = {'id':point.point_id, 'latitude':point.latitude, 'longitude':point.longitude}
            track_data.update({str(point.point_id) : point_data})
        data.update({str(track.track_id) : track_data})
    return data
            

