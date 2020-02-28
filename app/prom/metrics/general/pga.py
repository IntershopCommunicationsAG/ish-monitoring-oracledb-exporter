from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

NAME = '''name'''
VALUE = '''value'''


class PGA(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge('oracledb_pga'
            , 'Gauge metric to view PGA memory usage statistics (v$pgastat).'
            , labelnames=['server', 'port', 'type']
            , registry=registry)

        self.query = ('''
            SELECT
             name as %s
             , value AS %s
            FROM V$PGASTAT
        ''' % (NAME, VALUE))

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                self.metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), type=self.cleanName(row[NAME])) \
                    .set(row[VALUE])

