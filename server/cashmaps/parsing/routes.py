import os
from rq import get_current_job
from pathlib import Path

from flask import request, get_flashed_messages, flash, current_app

from cashmaps import db, queue
from cashmaps.tasks import start_task
from cashmaps.parsing import parsing_bp
from cashmaps.parsing.parsers.homeport_parser import parse_homeport
from cashmaps.parsing.utils import broadcast_start, broadcast_finished


@parsing_bp.route('/test')
def parser_text():
    return {}

@parsing_bp.route('/parser/_start_parse', methods=['POST'])
def parser_start_parse():
    """Begins a parse with the request's attached files."""
    files = request.files
    for i in range(0, len(files)):

        #Store each file in a temp directory, where they can be read from.
        #Must delete these files manually, done in current_app/tasks.py/cleanup_parse()
        f = files.get(str(i))
        start_parse(f)

    return {'success': True}


def start_parse(file):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_TEMP'], os.path.basename(file.filename))

    if current_app.config['TESTING'] == True:
        dest_file = open(filepath, 'w')
        file.save(dest_file)

        file.close()
        dest_file.close()
    else:
        file.save(filepath)
        file.close()


    job = start_task(
            func = parse_homeport,
            args = [filepath],
            metadata = {'filepath':filepath},
            callback = parse_callback,
            callback_args = [filepath],
            exc_callback = parse_exc_callback,
            exc_callback_args = [filepath]
    )

    broadcast_start(job.id, os.path.basename(filepath))

    return job


def parse_callback(filepath):
    job = get_current_job()

    broadcast_finished(job.get_id(), os.path.basename(filepath))
    print(db.session.new)

    os.remove(filepath)
    

def parse_exc_callback(job, exc_type, exc_message, traceback, filepath):
    print(db.session.new)
    db.session.rollback()

    os.remove(filepath)

