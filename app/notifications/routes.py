from app.notifications import notifications_bp
from flask import request
from flask_socketio import emit
from app import socketio

import datetime

def send_notification(message_type, message):
    data = {
        'message': message,
        'timestamp': str(datetime.datetime.utcnow())
    }
    socketio.emit(message_type, data, broadcast=True, namespace='/notifications')
