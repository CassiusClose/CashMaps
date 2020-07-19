from cashmaps import app, db
from cashmaps.models import results_to_arr
import PIL
from PIL import Image

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    absolute_filepath = db.Column(db.String(256), unique=True)
    relative_filepath = db.Column(db.String(256), unique=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def to_dict(self):
        return {'id':self.id, 'filepath':self.relative_filepath, 'width':self.width, 'height':self.height}

    def save_photo_to_db(abs_filepath, rel_filepath):
        image = Image.open(abs_filepath)
        print(image.size)
        obj = Photo(absolute_filepath=abs_filepath, relative_filepath=rel_filepath)
        db.session.add(obj)
        db.session.commit()

    def get_photo_by_abs_filepath(filepath):
        return Photo.query.filter_by(absolute_filepath=filepath).first()

    def get_photo_by_rel_filepath(filepath):
        return Photo.query.filter_by(relative_filepath=filepath).first()

    def get_photos():
        return {'photos': results_to_arr(Photo.query.all())}
