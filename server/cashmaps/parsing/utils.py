from cashmaps import socketio
from flask import current_app

socket = None


def broadcast_start(job_id, filename):
    data = {
        'job_id': job_id,
        'progress': 0,
        'max_progress': 100, 'filename': filename
    }
    socketio.emit('parser_start', data, broadcast=True, namespace='/parsers')


def broadcast_progress(job_id, progress, max_progress, filename):
    data = {
        'job_id': job_id,
        'progress': progress,
        'max_progress': max_progress,
        'filename': filename
    }
    socketio.emit('parser_update', data, broadcast=True, namespace='/parsers')


def broadcast_error(job_id, filename):
    data = {
        'job_id': job_id,
        'filename': filename
    }
    socketio.emit('parser_error', data, namespace='/parsers')


def broadcast_finished(job_id, filename):
    data = {
        'job_id': job_id,
        'filename': filename
    }
    socketio.emit('parser_finish', data, namespace='/parsers')
