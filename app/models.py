from app import app, db
from app import redis as redis_conn
import redis
from datetime import datetime
import rq

#Be careful of ForeignKey case! 'ForeignKey' would become 'foreign_key'. Underscores
#are kept

class Track(db.Model):
    """A database model that stores a track, which is a collection of points"""

    database_id = db.Column(db.Integer, primary_key=True)

    track_id = db.Column(db.Integer)

    #Relates this track to its list of points
    points = db.relationship('TrackPoint', backref='track', lazy='dynamic')

class TrackPoint(db.Model):
    """A database model that stores points on a map, lat long, that make up tracks"""

    database_id = db.Column(db.Integer, primary_key=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, unique=True, index=True)

    #Links this point to its track
    track_id = db.Column(db.Integer, db.ForeignKey('track.database_id'))


class Task(db.Model):
    job_id = db.Column(db.String(64), primary_key=True)
    job_type = db.Column(db.String(64), index=True)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.job_id, connection=redis_conn)
            rq_job.refresh()
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            print("REDIS Exception")
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100

    def get_max_progress(self):
        job = self.get_rq_job()
        return job.meta.get('max_progress', 100) if job is not None else 100

    def get_meta(self, meta):
        job = self.get_rq_job()
        return job.meta.get(meta) if job is not None else None

    def to_dict(self):
        data = {'job_id':self.job_id, 'job_type':self.job_type}
        if(self.job_type == app.config['TASK_TYPE_PARSE']):
            data['filename'] = self.get_meta('filename')
            data['progress'] = self.get_progress()
            data['max_progress'] = self.get_max_progress()
        return data

    def results_to_dict(results):
        dict = {}
        i = 0
        for task in results:
            dict[str(i)] = task.to_dict()
            i+=1
        return dict


    def get_tasks_by_type(type):
        tasks = Task.query.filter_by(job_type=type)
        return Task.results_to_dict(tasks)
    



class FlashMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String(64), index=True)
    message = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True)

    def to_dict(self):
        return {'id':self.id, 'message_type':self.message_type, 'message':self.message, 'timestamp':self.timestamp}

    def results_to_dict(arr):
        dict = {}
        i = 0
        for obj in arr:
            dict[str(i)] = obj.to_dict() 
            i +=1
        return dict


    def create_message(message, type):
        obj = FlashMessage(message=message, timestamp=datetime.utcnow(), message_type = type)
        db.session.add(obj)
        db.session.commit()

    def get_messages():
        messages = FlashMessage.query.order_by(FlashMessage.timestamp.desc())
        dict = FlashMessage.results_to_dict(messages)

        FlashMessage.query.delete()
        db.session.commit()
        return dict 

    def get_messages_by_type(type):
        messages = db.session.query(FlashMessage).filter_by(message_type=type).order_by(FlashMessage.timestamp.desc())

        dict = FlashMessage.results_to_dict(messages)

        FlashMessage.query.filter_by(message_type=type).delete()
        db.session.commit()
        return dict 

