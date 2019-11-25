"""Bootstrap app"""
import logging
import os

from flask import Flask
from flask_apscheduler import APScheduler
# Defines the format of the logging to include the time and to use the INFO logging level or worse.
from cx_Oracle import OperationalError
from pythonjsonlogger import jsonlogger

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

logHandler = logging.StreamHandler()
format_str = '%(asctime)%(levelname)%(filename)%(funcName)20s%(message)'
formatter = jsonlogger.JsonFormatter(format_str)
logHandler.setFormatter(formatter)
LOGGER.addHandler(logHandler)

scheduler = APScheduler()


def create_app():
    """
    Flask application factory that creates app instances.
    Every time this function is called, a new application instance is created. The reason
    why an application factory is needed is because we need to use different configurations
    for running our tests.
    :return Flask object: Returns a Flask application instance
    """
    app = Flask(__name__)

    # Set default config to test
    app_settings = os.getenv('FLASK_CONFIG', 'config.TestingConfig')
    LOGGER.info('Config set: %s', app_settings)
    app.config.from_object(app_settings)

    from app.controllers.main_routes import main_blueprint
    app.register_blueprint(main_blueprint)

    from app.controllers.metric_routes import metric_blueprint
    app.register_blueprint(metric_blueprint)

    # scheduler application
    scheduler.init_app(app)

    # prom extension
    from app.prom.prom_init import PromInitializer
    app.prom_init = PromInitializer(app)

    # Start after app is created, manage.py calls it even when in testing, so should be avoided
    if not app.testing:
        scheduler.start()
        # collect immediately
        try:
            app.prom_init.collector.collect(app)
            # schedule next
            scheduler.add_job(id='exporter_1',
                              func=app.prom_init.collector.collect,
                              args=[app],
                              trigger='interval',
                              seconds=app.config['COLLECT_METRICS_INTERVAL_SEC'])
        except AttributeError:
            LOGGER.info("No connection to oracle datasource")
        except OperationalError as e:
            LOGGER.info("Exception for the first time when connecting to database: %s", str(e))

    return app


if __name__ == '__main__':
    # Used for debugging in pycharm, if calling manage.py, break point does not stop
    create_app().run(debug=True, use_reloader=False)
