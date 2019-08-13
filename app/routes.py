from app import app, db, queue
from flask import render_template, jsonify, flash, redirect, url_for, request

#Can't stop static files from getting intercepted here as a catch-all,
#so just use the manual approach..
@app.route('/')
@app.route('/parser')
@app.route('/files')
@app.route('/map')
def catch_all():
    return render_template('dist/index.html')


#-Misc
@app.after_request
def after_request(response):
    """A method called after every url request is processed. Disables caching."""


    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
