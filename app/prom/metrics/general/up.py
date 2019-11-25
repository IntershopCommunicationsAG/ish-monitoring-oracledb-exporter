import logging

from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric
from app.prom.database import util as db_util

UP = '''oracledb_up'''

LOGGER = logging.getLogger(__name__)


class Up(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.is_up_metric = True

        self.metric = Gauge('oracledb_up', 'Oracle exporter UP status', registry=registry)

        super().__init__()

    def collect(self, app):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """

        with app.app_context():
            if db_util.is_port_open():
                self.metric.set(1)
                LOGGER.info("OracleDB is UP")
            else:
                self.metric.set(0)
                LOGGER.info("OracleDB is DOWN")
