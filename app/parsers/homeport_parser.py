import re
import logging as log
import os
from flask import abort, flash
from app import db
from app.models import Track, TrackPoint
from sqlalchemy import exc
import datetime
import threading

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


class Homeport_Parser(threading.Thread):
    #The categories the track file is separated into
    categories = ['metadata', 'author', 'copyright', 'link', 'rte', 'retpt', 'wpt', 'Address', 'PhoneNumber', 'Categories', 'trk', 'trkseg', 'trkpt']

    def __init__(self, f):
        self.tracks = []
        self.f = f
        self.progress = 0
        self.max_progress = 100
        super().__init__()

    def run(self):
        """Parses a Garmin Homeport exported txt file and adds its data to the database"""

        #Open the file and read the contents
        #Encode with utf-8-sig otherwise there will be annoying whitespace characters
        try:
            contents = self.f.read().decode("utf-8-sig")
        except IOError:
            abort(404, "ERROR: Homeport Parser - File not found: " + filepath)
        
        #A handy regex expression to split the contents of the file by the items in
        #the categories list. The resulting strings do not contain the items that they
        #were split with.
        regex = r"\b(?:{})\b".format("|".join(self.categories))

        #split with regex
        strings = re.split(regex, contents)

        #The first string tends to be empty and should be removed. So far this is the
        #only one
        if(strings[0].isspace()):
            del strings[0]

        #Process each category seperately by calling their respective functions
        for i in range(0, len(self.categories)):
            log.info('\nProcessing ' + self.categories[i])

            #Uses a string to call a local function. Set up so each category has its own
            #HACKY, VERY HACKY
            try:
                eval('self.process_' + self.categories[i] + '(strings[' + str(i) + '])')
            except AttributeError or NameError:
                pass


        for t in self.tracks:
            print(len(Track.query.get(t.database_id).points.all()))
            if(len(Track.query.get(t.database_id).points.all()) == 0):
                db.session.delete(Track.query.get(t.database_id))
                db.session.commit()


    #-Functions to process each category
    #Most of these are ignored for now because the data is not relevant 

    def process_trk(self, string):
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
                continue 

            self.tracks.append(track)

            log.info("Created track with id " + str(id))

    def process_trkpt(self, string):
        """Initializes track points from the file and adds them to the database"""
        #split into lines and remove empty ones
        lines = string.split('\n')
        lines = removeEmptyFromList(lines)

        self.max_progress = len(lines)-1

        #start at 1 to ignore the titles, which aren't data
        for i in range(1, len(lines)):
            self.progress = i
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
            for t in self.tracks:
                if track_id == t.track_id:
                    track = t
                    break
            point = TrackPoint(track=track, latitude=latitude, longitude=longitude, timestamp=timestamp)
            db.session.add(point)
            try:
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                #log.error(e)
                log.error("Error: tried to add track point with the id of an existing point: " + str(id))
                continue

            log.info("Created point with id " + str(id))
