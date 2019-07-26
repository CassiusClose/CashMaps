import re
import logging as log
import os
from app import db
from flask import abort

log.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(message)s')


categories = ['metadata', 'author', 'copyright', 'link', 'rte', 'retpt', 'wpt', 'Address', 'PhoneNumber', 'Categories', 'trk', 'trkseg', 'trkpt']

reg_categories = []
for cat in categories:
    reg_categories.append(cat + '\n')

def process_file(filepath):
    try:
        track_file = open(filepath, 'r')
    except IOError:
        abort(404, "ERROR: Homeport Parser - File not found")
#        return None
    contents = track_file.read()
    contents = contents.decode("utf-8-sig")

    regex = r"\b(?:{})\b".format("|".join(categories))

    strings = re.split(regex, contents)

    if(strings[0].isspace()):
        del strings[0]

    for i in range(0, len(categories)):
        log.info('\nProcessing ' + categories[i])
        eval('process_' + categories[i] + '(strings[' + str(i) + '])')


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
    lines = string.split('\n')

    #For some reason, when these ifs are in the same for loop, the 'if not l' doesn't work
    for l in lines:
        if not l:
            lines.remove(l)
    for l in lines:
        if l.isspace():
            lines.remove(l)

    for i in range(1, len(lines)):
        attrs = lines[i].split('\t')
        id = int(attrs[0])
        log.info("Created track with id " + str(id))
        

def process_trkseg(string):
    log.info('Ignoring..')

def process_trkpt(string):
    log.info('Ignoring..')

#process_file('../static/resources/track.txt')
#process_file('app/static/resources/track.txt')
