from app import app, db, queue
from app.models import Task, FlashMessage
from rq import get_current_job
import os

def start_task(func, args, job_type, metadata={}):
    arg_list = [func, args, job_type, metadata]
    job = queue.enqueue_call(func=go, args=arg_list)

    progress = Task(job_id=job.get_id(), job_type=job_type)
    db.session.add(progress)
    db.session.commit()

    return job.get_id()

def go(func, args, job_type, metadata):
    job = get_current_job()

    for key in metadata:
        job.meta[key] = metadata[key]
    job.meta['callback'] = cleanup_task
    job.save_meta()

    func(*args)

    cleanup_task()

def cleanup_task():
    job_id = get_current_job().get_id()
    task = Task.query.filter_by(job_id=job_id).first()

    callback_switch = {
        'parse': cleanup_parse,
    }
    callback = callback_switch.get(task.job_type)
    if(callback):
        callback(task)


    db.session.delete(task)
    db.session.commit()

def cleanup_parse(task):
    os.remove(task.get_meta('filepath'))
    FlashMessage.create_message("Parse Complete: " + task.get_meta('filename'), app.config['TASK_TYPE_PARSE'])
