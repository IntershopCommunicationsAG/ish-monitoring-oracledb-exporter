import logging

from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

UP = '''oracledb_up'''

LOGGER = logging.getLogger(__name__)


class Up(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.is_up_metric = True

        self.metric = Gauge('oracledb_up'
            , 'Oracle exporter UP status'
            , labelnames=['server', 'port']
            , registry=registry)

        super().__init__()

    def collect(self, app):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """

        with app.app_context():
            if db_util.is_port_open():
                self.metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port()) \
                    .set(1)
                LOGGER.info("OracleDB is UP")
            else:
                self.metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port()) \
                    .set(0)
                LOGGER.info("OracleDB is DOWN")
