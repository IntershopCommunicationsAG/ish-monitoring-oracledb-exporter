from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

SID = '''sid'''
CLIENT_INFO = '''client_info'''
SEQUENCE = '''sequence'''
EVENT = '''event'''
STATE = '''state'''
WAITING_TIME = '''waiting_time'''


class RmanCurrBackupWaits(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge('oracledb_rman_curr_backup_event_waiting_time_sec'
            , 'Gauge metric with event waiting times of the current rman backup.'
            , labelnames=['server'
                          , 'port'
                          , 'sid'
                          , 'client_info'
                          , 'sequence'
                          , 'event'
                          , 'state'
                          ]
            , registry=registry)

        self.query = '''
        SELECT
         sid AS %s
         , CLIENT_INFO AS %s
         , seq# as %s
         , event AS %s
         , state AS %s
         , wait_time_micro/1000000 as %s
        FROM v$session
        WHERE
         program LIKE '%%rman%%'
         and wait_time = 0
         and not action is null
        ''' % (SID, CLIENT_INFO, SEQUENCE, EVENT, STATE, WAITING_TIME)

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
                    .labels(server=db_util.get_server(), port=db_util.get_port(), sid=row[SID], client_info=row[CLIENT_INFO], sequence=row[SEQUENCE], event=self.cleanName(row[EVENT]), state=row[STATE]) \
                    .set(row[WAITING_TIME])
