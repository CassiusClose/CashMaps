import pathlib
import pytest
import datetime
import os

from werkzeug.datastructures import FileStorage

from cashmaps import db
from cashmaps.map.models import *
from cashmaps.tests.fixtures import app, worker, browser
from cashmaps.parsing.parsers.homeport_parser import parse_homeport
from cashmaps.parsing.routes import start_parse
from flask import url_for


def get_testfile_path(filename):
    return pathlib.Path(__file__).parent.absolute() / 'testfiles' / filename


@pytest.mark.usefixtures('live_server')
class TestHomeportParser:

    def test_integ(self, app, browser, live_server):
        url = url_for('index', _external=True)

        browser.get(url)
        assert 'Cash Maps' in browser.title


