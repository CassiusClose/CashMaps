from app import app, db
from app import redis as redis_conn
import redis
from datetime import datetime
import rq

def results_to_arr(results):
    """Returns the results of a query() call as an array, with each object in a dictionary format"""
    arr = []
    for task in results:
        arr.append(task.to_dict())
    return arr 


class Task(db.Model):
    """Represents a redis queue task for easy access from the rest of the server"""

    #job_id should be the id gotten from the RQ job
    job_id = db.Column(db.String(64), primary_key=True)

    #job_type has constants set up in app.config
    job_type = db.Column(db.String(64), index=True)

    def cancel_if_nonactive(self):
        job = self.get_rq_job()
        if not job.is_started:
            self.get_rq_job().cancel()
            db.session.delete(self)
            db.session.commit()

    def to_dict(self):
        """Returns a dictionary representation of the object to be used as JSON."""
        data = {'job_id':self.job_id, 'job_type':self.job_type}

        #Depending on what type of job it is, a representation should have more data than is
        #available in the database model
        if(self.job_type == app.config['TASK_TYPE_PARSE']):
            data['filename'] = self.get_meta('filename')
            data['progress'] = self.get_progress()
            data['max_progress'] = self.get_max_progress()

        return data

    def get_rq_job(self):
        """Returns the associated RQ Job and refreshes the job."""
        try:
            rq_job = rq.job.Job.fetch(self.job_id, connection=redis_conn)
            rq_job.refresh()
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            print("REDIS Exception") #TODO better error message
            return None
        return rq_job

    def get_progress(self):
        """Returns the tasks progress"""
        job = self.get_rq_job()
        #If 'progress' isn't metadata, consider the job not started, return 0
        #If the job doesn't exist, consider it finished, return 100
        #TODO Doesn't quite make sense, because progress isn't always out of 100
        return job.meta.get('progress', 0) if job is not None else 100

    def get_max_progress(self):
        """Returns the tasks max amount of progress, what would be considered finished."""
        job = self.get_rq_job()
        #If 'max_progress' isn't metadata or job doesn't exist, return 100
        #TODO Doesn't make sense, because max_progress isn't always out of 100
        return job.meta.get('max_progress', 100) if job is not None else 100

    def get_meta(self, meta):
        """Returns the job's metadata associated with the given string, or None if it does not exist"""
        job = self.get_rq_job()
        #If job doesn't exist, return None
        return job.meta.get(meta) if job is not None else None


    def get_tasks_by_type(type):
        """Returns all the tasks of the given type in JSON format."""
        tasks = Task.query.filter_by(job_type=type)
        return {"tasks": results_to_arr(tasks)}
    
    def cancel_nonactive_tasks():
        tasks = Task.query.all()
        for task in tasks:
            task.cancel_if_nonactive()





class FlashMessage(db.Model):
    """Represents a flashed message as an alternative to flask's flash messaging system."""

    #SQLAlchemy-assigned id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #Currently also uses Task Type constants from app.config
    message_type = db.Column(db.String(64), index=True)
    message = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True)

    def to_dict(self):
        """Returns a dictionary representation of the object to be used as JSON."""
        return {'id':self.id, 'message_type':self.message_type, 'message':self.message, 'timestamp':self.timestamp}


    def create_message(message, type):
        """Creates a message object and adds it to the database."""
        obj = FlashMessage(message=message, timestamp=datetime.utcnow(), message_type = type)
        db.session.add(obj)
        db.session.commit()

    def get_messages():
        """Returns all messages in the database and removes them from the database."""
        messages = FlashMessage.query.order_by(FlashMessage.timestamp.desc())
        arr = results_to_arr(messages)
        for i in range(0, length(arr)):
            print(arr[i]);

        FlashMessage.query.delete()
        db.session.commit()
        return {"messages": arr}

    def get_messages_by_type(type):
        """Returns all messages of a certain type and removes them from the database."""
        messages = db.session.query(FlashMessage).filter_by(message_type=type).order_by(FlashMessage.timestamp.desc())

        arr = results_to_arr(messages)

        FlashMessage.query.filter_by(message_type=type).delete()
        db.session.commit()
        return {"messages": arr}
