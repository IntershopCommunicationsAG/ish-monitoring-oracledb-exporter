from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric
from app.prom.database import util as db_util

from cx_Oracle import InterfaceError

UP = '''oracledb_up'''


class Up(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge('oracledb_up', 'Oracle exporter UP status', registry=registry)

        super().__init__()

    def collect(self):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        try:
            db_util.get_connection()
            self.metric.set(1)
        except InterfaceError:
            self.metric.set(0)
