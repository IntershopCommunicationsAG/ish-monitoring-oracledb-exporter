from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

METRIC_NAME = '''metric_name'''
VALUE = '''value'''


class SysMetric(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge('oracledb_sysmetric',
                        'Gauge metric with read/write pysical IOPs/bytes (v$sysmetric).',
                        labelnames=['type'],
                        registry=registry)

        # 2092    Physical Read Total IO Requests Per Sec
        # 2093    Physical Read Total Bytes Per Sec
        # 2100    Physical Write Total IO Requests Per Sec
        # 2124    Physical Write Total Bytes Per Sec
        self.query = ('''
        SELECT metric_name AS %s, value AS %s
        FROM v$sysmetric
        WHERE metric_id IN (2092,2093,2124,2100)
        ''' % (METRIC_NAME, VALUE))

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(type=self.cleanName(row[METRIC_NAME])) \
                .set(row[VALUE])

