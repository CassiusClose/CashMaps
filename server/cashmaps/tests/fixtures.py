import os 
import tempfile
import time
import pytest
from rq import SimpleWorker, get_current_job
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from config import TestConfig
from cashmaps import db, queue, create_app
from cashmaps.tasks import task_exception_handler
from flask import current_app


@pytest.fixture(scope='session')
def app():
    """
    Creates an instance of the Flask app using the factory function.
    """
    app = create_app(TestConfig)

    #Pass app context along to the test using this fixture
    with app.app_context(): 
        return app


@pytest.fixture
def database(app):
    """
    Initializes the server's database, and cleans it up afterward
    """
    with app.app_context():
        db.create_all()

        yield db

        db.session.remove()
        db.drop_all()


@pytest.fixture
def worker():
    """
    Creates an RQ worker, set up the same way it would be with the actual
    server running. Does not actually start the worker working.
    """
    worker = SimpleWorker([queue], connection=queue.connection,
            exception_handlers=[task_exception_handler],
            disable_default_exception_handler=True)
    return worker


@pytest.fixture
def browser():
    """
    Creates a headless Selenium browser, and cleans it up afterward.
    """
    options = Options()
    options.headless = True
    browser = Firefox(options=options)

    yield browser

    browser.implicitly_wait(1)
    browser.quit()
