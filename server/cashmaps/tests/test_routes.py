import pathlib
import pytest
import datetime
import os

from werkzeug.datastructures import FileStorage

from cashmaps import db, queue
from cashmaps.tasks import start_task
from cashmaps.map.models import *
from cashmaps.tests.fixtures import app, worker, browser, database
from cashmaps.parsing.parsers.homeport_parser import parse_homeport
from cashmaps.parsing.routes import start_parse

from flask import url_for

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures('live_server')
class TestRoutes:
    """
    Tests that each possible URL route of the application returns the right
    page.
    """

    def est_route_homepage(self, browser):
        """
        Tests that the index/homepage route returns the right page.
        """
        browser.get(url_for('index', _external=True))
        assert 'Cash Maps' in browser.title
        assert 'Homepage' in browser.page_source


    def est_route_parsers(self, browser):
        """
        Tests that the parser route returns the right page.
        """
        browser.get(url_for('parser', _external=True))
        assert 'Cash Maps' in browser.title
        assert 'Active Parse Tasks' in browser.page_source


    def test_route_map(self, browser, database):
        """
        Tests that the map route returns the right page.
        """
        browser.get(url_for('map', _external=True))
        assert 'Cash Maps' in browser.title

        #element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "cesiumMap")))


def func():
    pass

class TestPostCalls:
    """
    Tests misc POST routes that let the client perform certain tasks.
    """

    def test_rq_clear(self, app):
        """
        '/_rq_clear' clears the Redis Queue, used to clear up stale RQ jobs generated
        in developments.
        """
        queue.empty()
        client = app.test_client()
        job = start_task(func)

        assert len(queue.jobs) == 1

        client.post('/_clear_rq')

        assert len(queue.jobs) == 0

