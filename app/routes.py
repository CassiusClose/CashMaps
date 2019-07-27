from app import app, db, data_compiler
from flask import render_template, jsonify
from app.parsers import homeport_parser
from app.models import Track, TrackPoint

@app.route('/')
@app.route('/index')
def index():
    return render_template('header.html')

@app.route('/map')
def map():
    """Routes the page with the Cesium map"""

    return render_template('map.html')

@app.route('/parser')
def parser():
    """Routes the page that lets you parse track data files"""

    #Process the specified file, just an example for now
    homeport_parser.process_file('app/static/resources/track.txt')
    return render_template('header.html') 

#-Routes below here do not redirect to a new web page. I'm not sure what that's called.

@app.route('/_get_data', methods=['POST'])
def get_data():
    """Passes track data along to the Cesium widget to be displayed"""

    point_data = data_compiler.get_track_data()
    return jsonify(point_data)



#-Misc

@app.after_request
def after_request(response):
    """A method called after every url request is processed. Disables caching."""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
