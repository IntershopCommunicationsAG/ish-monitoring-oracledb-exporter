from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''


class Process(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'oracledb_process_count'
            , 'Gauge metric with count of processes.'
            , labelnames=['server', 'port']
            , registry=registry)
        self.query = '''
            SELECT COUNT(*) as %s FROM v$process
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
