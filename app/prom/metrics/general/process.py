from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''


class Process(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'oracledb_process_count',
            'Gauge metric with count of processes.',
            registry=registry)
        self.query = '''
        SELECT COUNT(*) as %s FROM v$process
        ''' % COUNT

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        self.metric.set(next(rows)[COUNT])
