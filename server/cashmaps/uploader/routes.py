from cashmaps import app, db
#TODO is photo_uploader necessary?
from cashmaps.uploader import uploader_bp, photo_uploader
from cashmaps.uploader.models import Photo
from flask import request
import os

@uploader_bp.route('/_upload_photo', methods=['POST'])
def upload_photo():
    filepath = request.form.get('filepath')
    overwrite = request.form.get('overwrite')

    for i in range(0, len(request.files)):
        save_photo_to_system(request.files[str(i)], filepath, overwrite)

    return {}

@uploader_bp.route('/_get_photos', methods=['POST'])
def uploader_get_photos():
    return Photo.get_photos()


def save_photo_to_system(f, filepath, overwrite):
    if(filepath.startswith('/')):
        filepath = filepath[1:]
    relativePath = os.path.join(filepath, f.filename)
    fullpath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER_PHOTOS'], relativePath))

    if Photo.get_photo_by_abs_filepath(fullpath) is not None:
        if overwrite == 'true':
            photo = Photo.get_photo_by_abs_filepath(fullpath)
            db.session.delete(photo)
            db.session.commit()
        else:
            return


    folderpath = os.path.dirname(fullpath)
    if not os.path.isdir(folderpath):
        os.makedirs(folderpath)

    f.save(fullpath)

    Photo.save_photo_to_db(fullpath, relativePath)
