from app import app
from flask import Blueprint
from flask_uploads import UploadSet, IMAGES

uploader_bp = Blueprint('uploader', __name__)

photo_uploader = UploadSet('photos', IMAGES)

from app.uploader import routes
