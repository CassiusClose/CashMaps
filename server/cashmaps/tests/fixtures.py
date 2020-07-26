import os 
import tempfile
import time
import pytest
from rq import SimpleWorker, get_current_job
from selenium.webdriver import Firefox

from config import Config
from cashmaps import db, queue, create_app
from cashmaps.tasks import task_exception_handler
from flask import current_app


@pytest.fixture(scope='session')
def app():
    app = create_app()

    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] =  False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config.get('BASEDIR'), 'cashmaps/static/resources/test_db.db')
    return app


@pytest.fixture
def database(app):
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config.get('BASEDIR'), 'cashmaps/static/resources/test_db.db')
        print(app.config)
        db.create_all()

        yield db

        db.session.remove()
        db.drop_all()


@pytest.fixture
def worker():
    worker = SimpleWorker([queue], connection=queue.connection,
            exception_handlers=[task_exception_handler],
            disable_default_exception_handler=True)
    return worker


@pytest.fixture
def browser():
    browser = Firefox()

    yield browser

    browser.implicitly_wait(1)
    browser.quit()
