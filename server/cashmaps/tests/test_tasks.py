import os 
import tempfile
import logging
import time
import pytest
import unittest
from rq import SimpleWorker, get_current_job
from rq.job import JobStatus

from config import Config
from cashmaps import app, db, queue
from cashmaps.tasks import start_task, task_exception_handler

from cashmaps.tests.fixtures import client


def start_worker():
    worker = SimpleWorker([queue], connection=queue.connection,
            exception_handlers=[task_exception_handler],
            disable_default_exception_handler=True)
    worker.work(burst=True)
    return worker


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
    def test_job_runs(self, client):
        """
        Test that a basic job function will complete when started with start_task(). Tests
        completion by reading the job's return value.
        """
        job = start_task(job_basic)
        start_worker()
        assert job.result == 'hi'


    def test_job_args(self, client):
        """
        Test that a job function recieves its arguments properly when started with start_task().
        Tests completion by reading the job's return value.
        """
        job = start_task(job_args, args=[3, 5])
        start_worker()
        assert job.result == 8


    def test_job_timeout(self, client):
        """
        Tests that a job started with start_task() will timeout after the timeout value passed
        to start_task().
        """
        job = start_task(job_sleep, timeout=1)
        start_worker()
        assert job.result == None
        assert job.get_status() == JobStatus.FAILED


    def test_job_receives_meta(self, client):
        """
        Test that metadata passed to start_task() will be accessible within the job function.
        """
        job = start_task(job_receive_meta, metadata={'1':'hi', '2':' there'})
        start_worker()
        assert job.result == 'hi there'


    def test_job_sends_meta(self, client):
        """
        Test that metadata set within a job will be available outside of the job.
        Make sure to call job.refresh(), which will pull any updates in meta.
        """
        job = start_task(job_send_meta)
        start_worker()
        job.refresh()
        assert job.result == 'hello'
        assert job.meta.get('test') == 'hi'

    
    def test_job_callback_no_args(self, client, capfd):
        """
        Test that a job started by start_task() will call the provided callback
        function when the job completes. Here, test a callback function that
        requires no arguments
        """
        job = start_task(job_basic, callback=callback)
        start_worker()
        out, err = capfd.readouterr()
        assert out == 'WOOHOO\n'
        assert job.result == 'hi'


    def test_job_callback_args(self, client, capfd):
        """
        Test that a job started by start_task() will call the provided callback
        function when the job completes. Here, test a callback function that
        requires arguments.
        """
        job = start_task(job_basic, callback=callback_args, callback_args=['hello'])
        start_worker()
        out, err = capfd.readouterr()
        assert out == 'hello\n'
        assert job.result == 'hi'


    def test_job_exception_callback_print_exc_message(self, client, capfd):
        """
        If an exception callback function is passed to start_task(), then the function
        should be called if an exception is raised in the job. It should be given information
        about the exception (type, message, traceback).
        """
        job = start_task(job_exception, exc_callback=exception_callback_print_value)
        start_worker()

        out, err = capfd.readouterr()
        assert out == "<class 'Exception'>\nThis is an error.\n"


    def test_job_exception_callback_print_meta(self, client, capfd):
        """
        If an exception callback function is passed to start_task(), then the function should
        be called if an exception is raised in the job. It should be given the instance of the
        job that caused the exception, and thus be able to access that job's metadata.
        """
        job = start_task(job_exception, metadata={'test':'hello'},
                exc_callback=exception_callback_print_meta)
        start_worker()

        out, err = capfd.readouterr()
        assert out == 'hello\n'


    def test_job_exception_callback_args(self, client, capfd):
        """
        If an exception callback function is passed to start_task(), then the function should
        be called if an exception is raised in the job. start_task() should accept additional
        arguments (apart from the job and exception data) and pass them along to the callback
        function.
        """
        job = start_task(job_exception, exc_callback=exception_callback_args,
                exc_callback_args=[3, 8])
        start_worker()

        out, err = capfd.readouterr()
        assert out == '11\n'

        
