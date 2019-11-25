"""
This is where all the general routes and controllers are defined.
"""

from flask import Blueprint
from flask import current_app as app
from flask import make_response

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/')
def index():
    return make_response()


@main_blueprint.route('/health')
def health():
    app.prom_init.up_gauge.set(1)
    return make_response()
