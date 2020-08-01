import os 
import tempfile
import logging
import time
import pytest
import unittest
from rq import SimpleWorker, get_current_job
from rq.job import JobStatus

from cashmaps import db, queue
from cashmaps.tests.fixtures import app, worker
from cashmaps.tasks import start_task



def job_basic():
    return 'hi'

def job_args(a, b):
    return a + b

def job_sleep():
    time.sleep(2)
    return 'hi'

def job_receive_meta():
    job = get_current_job()
    return job.meta.get('1') + job.meta.get('2')

def job_send_meta():
    job = get_current_job()
    job.meta['test'] = 'hi'
    job.save_meta()
    return 'hello'

def job_exception():
    raise Exception("This is an error.")

def callback():
    print("WOOHOO")

def callback_args(string):
    print(string)

def exception_callback_print_value(job, exc_type, exc_value, traceback):
    print(exc_type)
    print(exc_value)

def exception_callback_print_meta(job, exc_type, exc_value, traceback):
    print(job.meta.get('test'))

def exception_callback_args(job, exc_type, exc_value, traceback, a, b):
    print(str(a + b))



class TestStartTask:
    """
    Tests all aspects of the start_task() function in cashmaps/tasks.py, which creates an RQ worker
    """
    def test_job_runs(self, worker):
        """
        Test that a basic job function will complete when started with start_task(). Tests
        completion by reading the job's return value.
        """
        job = start_task(job_basic)
        worker.work(burst=True)
       
        assert job.result == 'hi'


    def test_job_args(self, worker):
        """
        Test that a job function recieves its arguments properly when started with start_task().
        Tests completion by reading the job's return value.
        """
        job = start_task(job_args, args=[3, 5])
        worker.work(burst=True)

        assert job.result == 8


    def test_job_timeout(self, worker):
        """
        Tests that a job started with start_task() will timeout after the timeout value passed
        to start_task().
        """
        job = start_task(job_sleep, timeout=1)
        worker.work(burst=True)

        assert job.result == None
        assert job.get_status() == JobStatus.FAILED


    def test_job_receives_meta(self, worker):
        """
        Test that metadata passed to start_task() will be accessible within the job function.
        """
        job = start_task(job_receive_meta, metadata={'1':'hi', '2':' there'})
        worker.work(burst=True)

        assert job.result == 'hi there'


    def test_job_sends_meta(self, worker):
        """
        Test that metadata set within a job will be available outside of the job.
        Make sure to call job.refresh(), which will pull any updates in meta.
        """
        job = start_task(job_send_meta)
        worker.work(burst=True)

        job.refresh()
        assert job.result == 'hello'
        assert job.meta.get('test') == 'hi'

    
    def test_job_callback_no_args(self, worker, capfd):
        """
        Test that a job started by start_task() will call the provided callback
        function when the job completes. Here, test a callback function that
        requires no arguments
        """
        job = start_task(job_basic, callback=callback)
        worker.work(burst=True)

        out, err = capfd.readouterr()
        assert out == 'WOOHOO\n'
        assert job.result == 'hi'


    def test_job_callback_args(self, worker, capfd):
        """
        Test that a job started by start_task() will call the provided callback
        function when the job completes. Here, test a callback function that
        requires arguments.
        """
        job = start_task(job_basic, callback=callback_args, callback_args=['hello'])
        worker.work(burst=True)

        out, err = capfd.readouterr()
        assert out == 'hello\n'
        assert job.result == 'hi'


    def test_job_exception_callback_print_exc_message(self, worker, capfd):
        """
        If an exception callback function is passed to start_task(), then the
        function should be called if an exception is raised in the job. It
        should be given information about the exception (type, message, traceback).
        """
        job = start_task(job_exception, exc_callback=exception_callback_print_value)
        worker.work(burst=True)

        out, err = capfd.readouterr()
        assert out == "<class 'Exception'>\nThis is an error.\n"


    def test_job_exception_callback_print_meta(self, worker, capfd):
        """
        If an exception callback function is passed to start_task(), then the
        function should be called if an exception is raised in the job. It
        should be given the instance of the job that caused the exception, and
        thus be able to access that job's metadata.
        """
        job = start_task(job_exception, metadata={'test':'hello'},
                exc_callback=exception_callback_print_meta)
        worker.work(burst=True)

        out, err = capfd.readouterr()
        assert out == 'hello\n'


    def test_job_exception_callback_args(self, worker, capfd):
        """
        If an exception callback function is passed to start_task(), then the
        function should be called if an exception is raised in the job.
        start_task() should accept additional arguments (apart from the job
        and exception data) and pass them along to the callback function.
        """
        job = start_task(job_exception, exc_callback=exception_callback_args,
                exc_callback_args=[3, 8])
        worker.work(burst=True)

        out, err = capfd.readouterr()
        assert out == '11\n'

        
