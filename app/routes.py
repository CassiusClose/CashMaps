from app import app, db, data_compiler
from flask import render_template, jsonify, flash, redirect, url_for, request
from app.parsers.homeport_parser import Homeport_Parser
from app.models import Track, TrackPoint
from app.forms import ParsingForm 
from werkzeug import secure_filename

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/parser', methods=['GET', 'POST'])
def parser():
    """Routes the page that lets you parse track data files"""

    #Process the specified file, just an example for now
    #homeport_parser.process_file('app/static/resources/track.txt')
    form = ParsingForm()
    if form.validate_on_submit():
        for f in form.uploader.data:
            filename = secure_filename(f.filename)
            global parser
            parser = Homeport_Parser(f)
            parser.start()
        return 'h'

    return render_template('parsers.html', form=form, progress=request.args.get('progress'))


@app.route('/parseProgress')
def parseProgress():
    return render_template('parseProgress.html')




#-Routes below here do not redirect to a new web page. I'm not sure what that's called.

@app.route('/_get_data', methods=['POST'])
def get_data():
    """Passes track data along to the Cesium widget to be displayed"""

    point_data = data_compiler.get_track_data()
    return jsonify(point_data)

@app.route('/parser/_get_progress', methods=['POST'])
def get_progress():
    return {'max':parser.max_progress, 'progress':parser.progress, 'redirect_url':url_for('parser')}

@app.route('/parser/_parse_done', methods=['POST'])
def parse_done():
    print('what')
    flash("Parse done: " + parser.f.filename)
    return 'hi' 
    

#-Misc

@app.after_request
def after_request(response):
    """A method called after every url request is processed. Disables caching."""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
