import re
import logging as log
import os
from flask import abort
from app import db
from app.models import Track, TrackPoint
from sqlalchemy import exc

log.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(message)s')


categories = ['metadata', 'author', 'copyright', 'link', 'rte', 'retpt', 'wpt', 'Address', 'PhoneNumber', 'Categories', 'trk', 'trkseg', 'trkpt']

reg_categories = []
for cat in categories:
    reg_categories.append(cat + '\n')

def process_file(filepath):
    try:
        track_file = open(filepath, 'r', encoding="utf-8-sig")
    except IOError:
        abort(404, "ERROR: Homeport Parser - File not found")
#        return None
    contents = track_file.read()

    regex = r"\b(?:{})\b".format("|".join(categories))

    strings = re.split(regex, contents)

    if(strings[0].isspace()):
        del strings[0]

    for i in range(0, len(categories)):
        log.info('\nProcessing ' + categories[i])
        eval('process_' + categories[i] + '(strings[' + str(i) + '])')


def removeEmptyFromList(lines):
    #Any that are empty or just spaces are not added to the new form of list
    return [l for l in lines if not (not l or l.isspace())]


def process_metadata(string):
    print(string)
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
    lines = string.split('\n')

    lines = removeEmptyFromList(lines)

    for i in range(1, len(lines)):
        attrs = lines[i].split('\t')
        id = int(attrs[0])
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
    lines = string.split('\n')
    lines = removeEmptyFromList(lines)

    for l in lines:
        print(l)

    for i in range(1, len(lines)):
        attrs = lines[i].split('\t')
        id = int(attrs[0])
        track_id = int(attrs[1])
        latitude = float(attrs[2])
        longitude = float(attrs[3])

        point = TrackPoint(point_id=id, track=Track.query.get(track_id), \
                latitude=latitude, longitude=longitude)
        db.session.add(point)

        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            log.error("Error: tried to add track point with the id of an existing point")

        log.info("Created point with id " + str(id))

#process_file('../static/resources/track.txt')
#process_file('app/static/resources/track.txt')
