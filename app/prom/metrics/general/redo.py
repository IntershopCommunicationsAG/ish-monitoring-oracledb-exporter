from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''


class Redo(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'oracledb_redo_log_switches'
            , 'Gauge metric with Redo log switches over last 5 min (v$log_history).'
            , labelnames=['server', 'port']
            , registry=registry)
        self.query = '''
            SELECT count(*) AS %s
            FROM v$log_history
            WHERE first_time > sysdate - 1/24/12
        ''' % COUNT

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            self.metric \
                .labels(server=db_util.get_server(), port=db_util.get_port()) \
                .set(next(rows)[COUNT])
