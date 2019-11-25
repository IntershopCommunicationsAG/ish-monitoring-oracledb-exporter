# -*- coding: utf-8 -*-

"""
This file defines the group of tests for the simple website routes.

You can run this test group file by running the application and
running 'docker-compose run --rm flask python manage.py test_one test_website'
in a separate terminal window.
"""

import logging
import os
from unittest import mock

from flask_testing import TestCase

from app import create_app, LOGGER

# Creates the Flask application object that we use to initialize things in the app.
os.environ['FLASK_CONFIG'] = 'config.TestingConfig'

# Creates a new instance of the Flask application. The reason for this
# is that we can't interrupt the application instance that is currently
# running and serving requests.

app = create_app()


class TestMetric(TestCase):

    def create_app(self):
        """
        Instructs Flask to run these commands when we request this group of tests to be run.
        """

        # Sets the configuration of the application to 'TestingConfig' in order
        # that the tests use db_test, not db_dev or db_prod.
        app.config.from_object('config.TestingConfig')

        # Sets the logger to only show ERROR level logs and worse. We don't want
        # to print a million things when running tests.
        LOGGER.setLevel(logging.ERROR)

        return app

    @mock.patch('app.controllers.metric_routes.current_app')
    def test_should_metric_prom_200(self, mock_app):
        with self.client:
            response = self.client.get('/metrics')
            self.assertEqual(response.status_code, 200)
