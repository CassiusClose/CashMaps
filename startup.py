from app import db
from app.models import Task

Task.query.delete()
db.session.commit()
