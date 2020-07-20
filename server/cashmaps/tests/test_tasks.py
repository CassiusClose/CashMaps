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
from cashmaps.tasks import start_task

from cashmaps.tests.fixtures import client


def start_worker():
    worker = SimpleWorker([queue], connection=queue.connection)
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

def callback():
    print("WOOHOO")

def callback_args(string):
    print(string)


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
