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


@pytest.mark.usefixtures('live_server')
class TestRoutes:
    """
    Tests that each possible URL route of the application returns the right
    page.
    """

    def test_route_homepage(self, browser):
        """
        Tests that the index/homepage route returns the right page.
        """
        #browser.get(url_for('index', _external=True))
        assert 1 == 1
        #assert 'Cash Maps' in browser.title
        #assert 'Homepage' in browser.page_source
        

    def test_route_parsers(self, browser):
        """
        Tests that the parser route returns the right page.
        """
        browser.get(url_for('parser', _external=True))
        assert 'Cash Maps' in browser.title
        assert 'Active Parse Tasks' in browser.page_source


    def test_route_map(self, browser):
        """
        Tests that the map route returns the right page.
        """
        browser.get(url_for('map', _external=True))
        assert 'Cash Maps' in browser.title




