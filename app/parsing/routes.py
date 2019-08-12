from app import app, db, queue
from app.tasks import start_task
from app.parsing import parsing_bp
from app.models import Task, FlashMessage
from app.parsing.parsers.homeport_parser import parse_homeport
from flask import request, get_flashed_messages, flash
import os

@parsing_bp.route('/parser/_start_parse', methods=['POST'])
def parser_start_parse():
    files = request.files
    ids = {} 
    for i in range(0, len(files)):

        f = files.get(str(i))
        filepath = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], f.filename)
        f.save(filepath)

        job_id = start_task(func=parse_homeport, args=(filepath,), job_type=app.config['TASK_TYPE_PARSE'], metadata={'filename':f.filename, 'filepath':filepath}) 

    return {}


@parsing_bp.route('/parser/_get_progress', methods=['POST'])
def parser_get_progress(): 
    return Task.get_tasks_by_type(app.config['TASK_TYPE_PARSE'])

@parsing_bp.route('/parser/_get_flashed_messages', methods=['POST'])
def parser_get_flashed_messages():
    return FlashMessage.get_messages_by_type(app.config['TASK_TYPE_PARSE'])
