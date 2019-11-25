# -*- coding: utf-8 -*-

"""
This file tests the various configurations of the Flask app.

It's pretty standard and shouldn't really be modified, unless you add
new configurations.
"""
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app

# Creates the Flask application object that we use to initialize things in the app.
os.environ['FLASK_CONFIG'] = 'config.TestingConfig'

app = create_app()


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
