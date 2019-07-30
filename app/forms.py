from flask_wtf import FlaskForm
from wtforms import SubmitField, MultipleFileField

class ParsingForm(FlaskForm):
    uploader = MultipleFileField('Upload track data', validators=[])
    submit = SubmitField('Parse')
