from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

METRIC_NAME = '''metric_name'''
VALUE = '''value'''


class CacheHitRatio(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge('oracledb_cachehitratio',
                        'Gauge metric with cache hit ratios (v$sysmetric).',
                        labelnames=['type'],
                        registry=registry)

        # 2000    Buffer Cache Hit Ratio
        # 2050    Cursor Cache Hit Ratio
        # 2112    Library Cache Hit Ratio
        # 2110    Row Cache Hit Ratio
        # 2115    PGA Cache Hit
        self.query = ('''
        SELECT metric_name AS %s, value AS %s
        FROM v$sysmetric
        WHERE group_id=2 AND metric_id IN (2000, 2050, 2112, 2110, 2115)
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

