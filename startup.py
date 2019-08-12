from app import db
from app.models import Task, FlashMessage

Task.query.delete()
FlashMessage.query.delete()
db.session.commit()
