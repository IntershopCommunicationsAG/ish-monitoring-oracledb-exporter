from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

NAME = '''name'''
VALUE = '''value'''


class InterConnect(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge('oracledb_interconnect',
                        'Gauge metric with interconnect block transfers (v$sysstat).',
                        labelnames=['name'],
                        registry=registry)

        self.query = ('''
        SELECT name AS %s, value AS %s
        FROM V$SYSSTAT
        WHERE name IN ('gc cr blocks served','gc cr blocks flushed','gc cr blocks received')
        ''' % (NAME, VALUE))

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(name=self.cleanName(row[NAME])) \
                .set(row[VALUE])

