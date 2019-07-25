from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('header.html')

@app.route('/map')
def map():
    return render_template('map.html')
