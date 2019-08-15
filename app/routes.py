from app import app, db, queue
from flask import render_template, jsonify, flash, redirect, url_for, request

#For this to work as a catchall, I couldn't stop it from also intercepting
#requests for static files such as .css files
#So I'm using a manual approach
@app.route('/')
@app.route('/parser')
@app.route('/files')
@app.route('/map')
def catch_all():
    return render_template('dist/index.html')


@app.after_request
def after_request(response):
    """A method called after every url request is processed. Disables caching."""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
