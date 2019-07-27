import re
import logging as log
import os
from flask import abort
from app import db
from app.models import Track, TrackPoint
from sqlalchemy import exc


#The categories the track file is separated into
categories = ['metadata', 'author', 'copyright', 'link', 'rte', 'retpt', 'wpt', 'Address', 'PhoneNumber', 'Categories', 'trk', 'trkseg', 'trkpt']


def process_file(filepath):
    """Parses a Garmin Homeport exported txt file and adds its data to the database"""

    #Open the file and read the contents
    #Encode with utf-8-sig otherwise there will be annoying whitespace characters
    try:
        track_file = open(filepath, 'r', encoding="utf-8-sig")
        contents = track_file.read()
    except IOError:
        abort(404, "ERROR: Homeport Parser - File not found: " + filepath)
    
    #A handy regex expression to split the contents of the file by the items in
    #the categories list. The resulting strings do not contain the items that they
    #were split with.
    regex = r"\b(?:{})\b".format("|".join(categories))

    #split with regex
    strings = re.split(regex, contents)

    #The first string tends to be empty and should be removed. So far this is the
    #only one
    if(strings[0].isspace()):
        del strings[0]

    #Process each category seperately by calling their respective functions
    for i in range(0, len(categories)):
        log.info('\nProcessing ' + categories[i])

        #Uses a string to call a local function. Set up so each category has its own
        #function
        eval('process_' + categories[i] + '(strings[' + str(i) + '])')


#-Helper Functions

def removeEmptyFromList(lines):
    #Any lines that are empty or only spaces are not added to the return list
    return [l for l in lines if not (not l or l.isspace())]


#-Functions to process each category
#Most of these are ignored for now because the data is not relevant 

def process_metadata(string):
    log.info('Ignoring..')

def process_author(string):
    log.info('Ignoring..')

def process_copyright(string):
    log.info('Ignoring..')

def process_link(string):
    log.info('Ignoring..')

def process_rte(string):
    log.info('Ignoring..')

def process_retpt(string):
    log.info('Ignoring..')

def process_wpt(string):
    log.info('Ignoring..')

def process_Address(string):
    log.info('Ignoring..')

def process_PhoneNumber(string):
    log.info('Ignoring..')

def process_Categories(string):
    log.info('Ignoring..')

def process_trk(string):
    """Initializes the file's tracks"""

    #split into lines and remove empty ones
    lines = string.split('\n')
    lines = removeEmptyFromList(lines)

    #ignore first line because that's titles, not actual data
    for i in range(1, len(lines)):
        #Each attribute is separated by a tab, so seperate by tabs
        attrs = lines[i].split('\t')

        #The order of the attributes have to be hard-coded, sorry
        id = int(attrs[0])

        #Create the Track database object and add it to the database
        #Undo the changes if a uniqueness error is thrown
        #So right now, it'll only undo the current track
        track = Track(track_id=id)
        db.session.add(track)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            log.error("Error: tried to add track with the id of an existing track")
            return False

        log.info("Created track with id " + str(id))
        

def process_trkseg(string):
    log.info('Ignoring..')

def process_trkpt(string):
    """Initializes track points from the file and adds them to the database"""

    #split into lines and remove empty ones
    lines = string.split('\n')
    lines = removeEmptyFromList(lines)

    #start at 1 to ignore the titles, which aren't data
    for i in range(1, len(lines)):
        #Split into attributes, which are separated by tabs
        attrs = lines[i].split('\t')

        #Read in attributes, order has to be hard-coded
        id = int(attrs[0])
        track_id = int(attrs[1])
        latitude = float(attrs[2])
        longitude = float(attrs[3])

        #Create the database TrackPoint object and add it to the database
        #Undo the changes if a uniqueness error is thrown
        #So right now, it'll only undo the current point 
        point = TrackPoint(point_id=id, track=Track.query.get(track_id), \
                latitude=latitude, longitude=longitude)
        db.session.add(point)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            log.error("Error: tried to add track point with the id of an existing point")

        log.info("Created point with id " + str(id))
