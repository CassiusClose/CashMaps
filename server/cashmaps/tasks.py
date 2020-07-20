from cashmaps import app, db, queue
from cashmaps.utils import send_notification
from rq import get_current_job
from rq.timeouts import JobTimeoutException
import os
import logging


def start_task(func, args=[], metadata={}, timeout=720, callback=None, callback_args=[]):
    """Adds a task to the redis queue, and creates a SQL database entry for it

    Creates a redis queue job to complete the specified function, adds any
    metadata to it, and creates a SQL database entry for the task.

    :param func:        The function to be called as the task
    :param args:        (Optional) Any arguments to the the task function
    :param job_type:    (Optional) What kind of job this is, to put in the SQL
                        entry
    :param metadata:    (Optional) Any metadata to pass along to the job
    :param timeout:     (Optional) After what time should the job timeout

    :return: The associated RQ Job's id
    """


    #create the argument list for go() and enqueues the job
    arg_list = [func, args, metadata, callback, callback_args]
    job = queue.enqueue_call(func=go, args=arg_list, timeout=timeout)


    for key in metadata:
        job.meta[key] = metadata[key]
    job.save_meta()

    return job



def go(func, args, metadata, callback, callback_args):
    """Helper function for start_task(). Acts as the target of a redis queue job.

    This function acts as the target function when starting a task with redis
    queue. The real function to be called as the task is passed to this. This
    way, this function can set job metadata and cleanup after the task is
    finished. This lets the real function remain independent of this task setup.

    In short, the issue is that job metadata is erased (or in a different
    context somehow) once the job starts, so by making go() the job's target,
    we can set the job's metadata and have it stick for the actual function
    that is undertaking the job.


    :param func: The real task function. go() is just a helper to call this function.
    :param args: Arguments for the task function
    :param metadata: Metadata for the RQ job to have. Sets it before calling the task function.
    """
    
    job = get_current_job()
    job.refresh() # Fetch meta data set in start_task()

    return_val = func(*args)

    if callback:
        callback(*callback_args)

    return return_val
