from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

NAME = '''resource_name'''
CURRENT_UTILIZATION = '''current_utilization'''
LIMIT_VALUE = '''limit_value'''

class Resource(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.current_utilization_metric = Gauge('oracledb_resource_current_utilization',
                                      'Generic counter metric from v$resource_limit view in Oracle (current value).',
                                      labelnames=[NAME],
                                      registry=registry)
        self.limit_value_metric = Gauge(
            'oracledb_resource_limit_value',
            'Generic counter metric from v$resource_limit view in Oracle (limit value).',
            labelnames=[NAME],
            registry=registry)

        self.query = '''
        SELECT resource_name AS %s, current_utilization AS %s, limit_value as %s
        FROM v$resource_limit
        ''' % (NAME, CURRENT_UTILIZATION, LIMIT_VALUE)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.current_utilization_metric \
                .labels(resource_name=row[NAME]) \
                .set(row[CURRENT_UTILIZATION])

            # we also do have UNLIMITED values, but we're ignore them
            try:
                floatValue = float(row[LIMIT_VALUE])
                self.limit_value_metric \
                    .labels(resource_name=row[NAME]) \
                    .set(floatValue)
            except ValueError:
                pass
