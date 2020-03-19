from app import app, db, queue
from flask import render_template, jsonify, flash, redirect, url_for, request 

#For this to work as a catchall, I couldn't stop it from also intercepting
#requests for static files such as .css files
#So I'm using a manual approach
@app.route('/')
@app.route('/parser')
@app.route('/files')
@app.route('/map')
@app.route('/upload')
@app.route('/gallery')
@app.route('/tools')
def catch_all():
    return render_template('static/index.html')

@app.route('/_upload_photo', methods=['POST'])
def upload_photo():
    filepath = request.form.get('filepath')
    for i in range(0, len(request.files)):
        f = request.files.get(str(i))
        fullpath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER_PHOTOS'], filepath), f.filename)
        os.makedirs(fullpath)
        print(fullpath)
    return {}


@app.after_request
def after_request(response):
    """A method called after every url request is processed. Disables caching."""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
