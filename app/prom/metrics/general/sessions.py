from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

SESSIONS_STATUS = '''status'''
SESSIONS_TYPE = '''type'''
SESSIONS_COUNT = '''value'''


class Sessions(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge('oracledb_sessions'
            , 'Gauge metric with count of sessions by status and type.'
            , labelnames=['server'
                          , 'port'
                          , 'status'
                          , 'type'
                          ]
            , registry=registry)
        self.query = '''
            SELECT status AS %s, type AS %s, COUNT(*) as %s
            FROM v$session
            GROUP BY status, type
        ''' % (SESSIONS_STATUS, SESSIONS_TYPE, SESSIONS_COUNT)

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
                    .labels(server=db_util.get_server(), port=db_util.get_port(),status=row[SESSIONS_STATUS], type=row[SESSIONS_TYPE]) \
                    .set(row[SESSIONS_COUNT])
