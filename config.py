"""
This file stores all the possible configurations for the Flask app.
Changing configurations like the secret key or the database
url should be stored as environment variables and imported
using the 'os' library in Python.
"""
import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER = os.getenv('ORACLE_SERVER', 'localhost')
    PORT = os.getenv('ORACLE_PORT', 1521)
    SERVICE = os.getenv('ORACLE_SERVICE', 'ORCL12')
    USERNAME = os.getenv('ORACLE_USERNAME', 'system')
    PASSWORD = os.getenv('ORACLE_PASSWORD', 'YourStrong!Passw0rd')
    COLLECT_METRICS_INTERVAL_SEC = int(
        os.getenv('COLLECT_METRICS_INTERVAL_SEC', 120))
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False