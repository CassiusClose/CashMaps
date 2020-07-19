import os 
import tempfile

import pytest

from config import Config
from cashmaps import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(Config.basedir, 'test.db')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    db.session.remove()
    db.drop_all()



def test_test(client):
    assert 4 == 4
