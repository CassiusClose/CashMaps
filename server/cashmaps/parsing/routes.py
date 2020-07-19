from cashmaps import app, db, queue
from cashmaps.tasks import start_task
from cashmaps.parsing import parsing_bp
from cashmaps.parsing.parsers.homeport_parser import parse_homeport
from flask import request, get_flashed_messages, flash
import os

@parsing_bp.route('/parser/_start_parse', methods=['POST'])
def parser_start_parse():
    """Begins a parse with the request's attached files."""
    files = request.files
    for i in range(0, len(files)):

        #Store each file in a temp directory, where they can be read from.
        #Must delete these files manually, done in app/tasks.py/cleanup_parse()
        f = files.get(str(i))
        filepath = os.path.join(app.config['UPLOAD_FOLDER_TEMP'], f.filename)
        f.save(filepath)

        job_id = start_task(func=parse_homeport, args=(filepath,), job_type=app.config['TASK_TYPE_PARSE'], metadata={'filename':f.filename, 'filepath':filepath}) 

    return {}
