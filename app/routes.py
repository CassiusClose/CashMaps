from app import app
from flask import render_template
from app.parsers import homeport_parser

@app.route('/')
@app.route('/index')
def index():
    return render_template('header.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/parser')
def parser():
    homeport_parser.process_file('test.txt')
    return render_template('header.html')
