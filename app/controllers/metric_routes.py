"""
This is where all the metric routes and controllers are defined.
"""

from flask import Blueprint, current_app
from prometheus_client.exposition import make_wsgi_app

metric_blueprint = Blueprint('metric_blueprint', __name__)


@metric_blueprint.route('/metrics')
def metrics():
    return make_wsgi_app(current_app.prom_init.registry)
