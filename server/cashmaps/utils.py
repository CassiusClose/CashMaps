import os

from flask import current_app

def remove_temp_files():
    """
    Removes all files in the temp file directory. Used when clearing the Redis
    Queue - parsing jobs in the queue will have temp files associated with
    them, but clearing the queue will not dispose of those files.
    """
    dir = current_app.config['UPLOAD_FOLDER_TEMP']
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
