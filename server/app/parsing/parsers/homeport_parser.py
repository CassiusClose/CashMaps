import os
import re
import datetime
import threading
import logging as log

from flask import abort, flash
from sqlalchemy import exc
from rq import get_current_job

from app import db
from app.map.models import Track, TrackPoint
from app import socketio

def broadcast_progress(job_id, progress, max_progress, filename):
    data = {
        'job_id': job_id,
        'progress': progress,
        'max_progress': max_progress,
        'filename': filename
    }
    socketio.emit('parser_update', data, broadcast=True, namespace='/parsers')

def broadcast_finished(job_id):
    socketio.emit('parser_finish', {'job_id':job_id}, namespace='/parsers')
    

#-Helper Functions
def removeEmptyFromList(lines):
    #Any lines that are empty or only spaces are not added to the return list
    return [l for l in lines if not (not l or l.isspace())]

def get_timestamp(string):
    if not string:
        return None
    split1 = string.split('T')
    date = split1[0]
    time = split1[1][:-1]
    date_split = date.split('-') 
    time_split = time.split(':')
    year = int(date_split[0])
    month = int(date_split[1])
    day = int(date_split[2])
    hour = int(time_split[0])
    minute = int(time_split[1])
    second = int(time_split[2])
    return datetime.datetime(year, month, day, hour, minute, second) 


#The categories the track file is separated into
categories = ['metadata', 'author', 'copyright', 'link', 'rte', 'retpt', 'wpt', 'Address', 'PhoneNumber', 'Categories', 'trk', 'trkseg', 'trkpt']


#Using a callback here is annoying, it would be nice if rq had a way to
#implement callbacks after tasks
def parse_homeport(filepath):
    """Parses a Garmin Homeport exported txt file and adds its data to the database"""

    #Open the file and read the contents
    #Encode with utf-8-sig otherwise there will be annoying whitespace characters

    try:
        f = open(filepath, "r", encoding='utf-8-sig')
        contents = f.read()
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


    tracks = process_trk(strings[10])

    process_trkpt(strings[12], tracks)

    for t in tracks:
        print(len(Track.query.get(t.database_id).points.all()))
        if(len(Track.query.get(t.database_id).points.all()) == 0):
            db.session.delete(Track.query.get(t.database_id))
            db.session.commit()


    job = get_current_job()
    broadcast_finished(job.get_id())


    f.close()

#-Functions to process each category
#Most of these are ignored for now because the data is not relevant 

def process_trk(string):
    """Initializes the file's tracks"""

    tracks = []

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
            print("Error: tried to add track with the id of an existing track")
            continue 

        tracks.append(track)

        print("Created track with id " + str(id))

    return tracks

def process_trkpt(string, tracks):
    """Initializes track points from the file and adds them to the database"""

    job = get_current_job()

    #split into lines and remove empty ones
    lines = string.split('\n')
    lines = removeEmptyFromList(lines)

    broadcast_progress(job.get_id(), 0, len(lines)-1, job.meta['filename'])
    job.meta['max_progress'] = len(lines)-1
    job.meta['progress'] = 0
    job.get_id()
    job.meta['filename']

    job.save_meta()

    #start at 1 to ignore the titles, which aren't data
    for i in range(1, len(lines)):
        job.meta['progress'] = i
        broadcast_progress(job.get_id(), i, len(lines)-1, job.meta['filename'])
        job.save_meta()

        #Split into attributes, which are separated by tabs
        attrs = lines[i].split('\t')

        #Read in attributes, order has to be hard-coded
        id = int(attrs[0])
        track_id = int(attrs[1])
        latitude = float(attrs[2])
        longitude = float(attrs[3])
        timestamp = get_timestamp(attrs[5])

        #Create the database TrackPoint object and add it to the database
        #Undo the changes if a uniqueness error is thrown
        #So right now, it'll only undo the current point 
        #HACKY FOR NOW
        track = None
        for t in tracks:
            if track_id == t.track_id:
                track = t
                break
        point = TrackPoint(track=track, latitude=latitude, longitude=longitude, timestamp=timestamp)
        db.session.add(point)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            print("Error: tried to add track point with the id of an existing point: " + str(id))
            continue

        print("Created point with id " + str(id))
