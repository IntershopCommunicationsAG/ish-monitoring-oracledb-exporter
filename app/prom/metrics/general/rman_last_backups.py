from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

SESSION_KEY = '''session_key'''
INPUT_TYPE = '''input_type'''
STATUS = '''status'''
START_TIME = '''start_time'''
END_TIME = '''end_time'''
INPUT_BYTES = '''input_bytes'''
OUTPUT_BYTES = '''output_bytes'''
ELAPSED_SECONDS = '''elapsed_seconds'''


class RmanLastBackups(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge('oracledb_rman_last_backup_time_sec',
                            'Gauge metric with last rman backups.',
                            labelnames=[
                                'session_key',
                                'input_type',
                                'status',
                                'start_time',
                                'end_time',
                                'input_bytes',
                                'output_bytes'
                            ],
                            registry=registry)

        self.query = '''
        SELECT
         SESSION_KEY as %s
         , INPUT_TYPE as %s
         , STATUS as %s
         , TO_CHAR(START_TIME,'mm/dd/yy hh24:mi') as %s
         , TO_CHAR(END_TIME,'mm/dd/yy hh24:mi') as %s
         , input_bytes as %s
         , output_bytes as %s
         , elapsed_seconds as %s
        FROM V$RMAN_BACKUP_JOB_DETAILS
        ORDER BY session_key DESC
        FETCH FIRST 10 ROWS ONLY
        ''' % (SESSION_KEY, INPUT_TYPE, STATUS, START_TIME, END_TIME, INPUT_BYTES, OUTPUT_BYTES, ELAPSED_SECONDS)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(session_key=row[SESSION_KEY], input_type=row[INPUT_TYPE], status=row[STATUS], start_time=row[START_TIME], end_time=row[END_TIME], input_bytes=row[INPUT_BYTES], output_bytes=row[OUTPUT_BYTES]) \
                .set(row[ELAPSED_SECONDS])
