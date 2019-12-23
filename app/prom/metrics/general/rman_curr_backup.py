from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

SID = '''sid'''
CONTEXT = '''context'''
TIME_REMAINING = '''time_remaining_sec'''
SOFAR = '''sofar_bytes'''
TOTALWORK = '''totalwork_bytes'''


class RmanCurrBackup(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.time_remaining_metric = Gauge('oracledb_rman_curr_backup_est_time_remaining_sec',
                            'Gauge metric with estimated time remaining of the current rman backup.',
                            labelnames=[
                                'sid',
                                'context',
                                'start_time'
                            ],
                            registry=registry)
        self.sofar_metric = Gauge('oracledb_rman_curr_backup_sofar_bytes',
                            'Gauge metric with so far processed bytes of the current rman backup.',
                            labelnames=[
                                'sid',
                                'context',
                                'start_time'
                            ],
                            registry=registry)
        self.total_work_metric = Gauge('oracledb_rman_curr_backup_total_work_bytes',
                            'Gauge metric with the amount of total bytes to be processed by the current rman backup.',
                            labelnames=[
                                'sid',
                                'context',
                                'start_time'
                            ],
                            registry=registry)

        self.query = '''
        SELECT
         o.sid AS %s
         , o.context AS %s
         , o.TIME_REMAINING AS %s
         , o.sofar AS %s
         , o.totalwork AS %s
        FROM v$session_longops o
        WHERE o.opname LIKE 'RMAN%%'
        AND o.opname NOT LIKE '%%aggregate%%'
        AND o.totalwork != 0
        AND o.sofar <> o.totalwork
        ''' % (SID, CONTEXT, TIME_REMAINING, SOFAR, TOTALWORK)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.time_remaining_metric \
                .labels(sid=row[SID], context=row[CONTEXT]) \
                .set(row[TIME_REMAINING])
            self.sofar_metric \
                .labels(sid=row[SID], context=row[CONTEXT]) \
                .set(row[SOFAR])
            self.total_work_metric \
                .labels(sid=row[SID], context=row[CONTEXT]) \
                .set(row[TOTALWORK])
