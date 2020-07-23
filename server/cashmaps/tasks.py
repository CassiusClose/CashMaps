from cashmaps import app, db, queue
from cashmaps.utils import send_notification
from rq import get_current_job
from rq.timeouts import JobTimeoutException
import os
import logging


def start_task(func, args=[], metadata={}, timeout=720, callback=None, callback_args=[], exc_callback=None, exc_callback_args=[]):
    """
    Performs the given function in a separate thread by creating a RQ Job and giving it to the
    Redis queue. Optionally, will call another 'callback' function on completion of the first.
    A function can also be passed as an exception handler, should the job raise an error.

    RQ itself doesn't support callback functionality, so to allow for a callback function,
    this actually passes the below go() function as the function of the RQ job. RQ will start
    a new thread and call go(), which is passed both the main task function and the callback.
    Then it can call both.


    Parameters
    ----------
    func : function
        The function that contains the task to be completed.

    args : list, optional
        Arguments passed to the task function, func

    metadata : dictionary, optional
        Metadata to be saved in the Redis job's metadata

    timeout : int, optional
        After how many seconds should this job timeout

    callback : function, optional
        A function to be called after the task function (func) has completed

    callback_args : list, optional
        Arguments to the callback function (callback)

    exc_callback : function, optional
        A function to be called if the job raises an exception

    exc_callback_args: list, optional
        Arguments to the exception callback function (exc_callback)


    Returns
    -------
    job : rq.Job object
        The job created to perform the given task
    """


    #create the argument list for go() and enqueues the job
    arg_list = [func, args, callback, callback_args]
    job = queue.enqueue_call(func=go, args=arg_list, timeout=timeout)


    # Save any metadata passed in to the job's metadata
    for key in metadata:
        job.meta[key] = metadata[key]
    # Save custom exception handler data in the job's metadata
    job.meta['exc_callback'] = exc_callback
    job.meta['exc_callback_args'] = exc_callback_args
    job.save_meta()

    return job



def go(func, args, callback, callback_args):
    """
    Helper function for start_task(). Acts as the target of a redis queue job.

    This function acts as the target function when starting a task with RQ 
    The real 'task function' to be called is passed to this function. This
    lets a callback function be called when the 'task function' is completed. Otherwise,
    RQ doesn't provide support for callbacks on the completion of a job.

    Parameters
    ----------
    func : function
        The real task that this Redis job will complete

    args : list
        Arguments to the task function (func)

    calback : function
        A callback function to be called when the task function (func) has completed

    callback_args : list
        Arguments to the callback function

    """
    
    job = get_current_job()
    job.refresh() # Fetch meta data set in start_task()

    # Call the actual job function
    return_val = func(*args)

    if callback:
        callback(*callback_args)

    return return_val



def task_exception_handler(job, exc_type, exc_value, traceback):
    """
    If an exception is raised during a job, this handler will be called by the worker doing the
    job. Because exception handlers are specified to the worker, this is a general exception
    handler function that the worker will call. If the job was given a specific exception
    callback function in start_task(), this function will call that function.

    The exception callback function must have its four beginning arguments be:
        (job, exception_type, exception_value, traceback)

    The specific exception callback and arguments are stored in the job's metadata so they
    can be accessed in this function.

    Parameters
    ----------
    job : rq.Job
        The instance of RQ Job that raised this exception

    exc_type
        The type of Exception that was raised

    exc_value : String
        The exception message

    traceback
        The traceback of the exception
    """
    job.refresh() #Update any changes to metadata

    callback = job.meta.get('exc_callback')

    if not callback:
        return True # Pass along to other exception handlers, if there are any

    args = job.meta.get('exc_callback_args')
    if not args: # If no specified args, change args from None to []
        args = []
    
    # job and exception data passed to the specific exception handler
    args.insert(0, job)
    args.insert(1, exc_type)
    args.insert(2, exc_value)
    args.insert(3, traceback)

    callback(*args)
    return False # Don't pass to any more exception handlers

