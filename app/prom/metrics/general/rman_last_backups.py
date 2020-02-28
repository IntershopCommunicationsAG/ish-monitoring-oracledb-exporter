from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

SESSION_KEY = '''session_key'''
INPUT_TYPE = '''input_type'''
STATUS = '''status'''
ELAPSED_SECONDS = '''elapsed_seconds'''
INPUT_BYTES = '''input_bytes'''
OUTPUT_BYTES = '''output_bytes'''



class RmanLastBackups(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge('oracledb_rman_last_backup_time_sec'
            , 'Gauge metric with last rman backups.'
            , labelnames=['server'
                          , 'port'
                          , 'session_key'
                          , 'input_type'
                          , 'status'
                          ]
            , registry=registry)

        self.input_bytes_metric = Gauge('oracledb_rman_last_backup_input_bytes'
            , 'Gauge metric with the amount of input bytes processed by the last rman backup.'
            , labelnames=['server'
                          , 'port'
                          , 'session_key'
                          , 'input_type'
                          , 'status'
                          ]
            , registry=registry)

        self.output_bytes_metric = Gauge('oracledb_rman_last_backup_output_bytes'
            , 'Gauge metric with the amount of output bytes processed by the last rman backup.'
            , labelnames=['server'
                          , 'port'
                          , 'session_key'
                          , 'input_type'
                          , 'status'
                          ]
            , registry=registry)

        self.query = '''
            SELECT
             SESSION_KEY as %s
             , INPUT_TYPE as %s
             , STATUS as %s
             , elapsed_seconds as %s
             , input_bytes as %s
             , output_bytes as %s
            FROM V$RMAN_BACKUP_JOB_DETAILS
            ORDER BY session_key DESC
            FETCH FIRST 10 ROWS ONLY
        ''' % (SESSION_KEY, INPUT_TYPE, STATUS, ELAPSED_SECONDS, INPUT_BYTES, OUTPUT_BYTES)

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                if row[ELAPSED_SECONDS] is not None:
                    self.metric \
                        .labels(server=db_util.get_server(), port=db_util.get_port(), session_key=row[SESSION_KEY], input_type=row[INPUT_TYPE], status=row[STATUS]) \
                        .set(row[ELAPSED_SECONDS])
                if row[INPUT_BYTES] is not None:
                    self.input_bytes_metric \
                        .labels(server=db_util.get_server(), port=db_util.get_port(), session_key=row[SESSION_KEY], input_type=row[INPUT_TYPE], status=row[STATUS]) \
                        .set(row[INPUT_BYTES])
                if row[OUTPUT_BYTES] is not None:
                    self.output_bytes_metric \
                        .labels(server=db_util.get_server(), port=db_util.get_port(), session_key=row[SESSION_KEY], input_type=row[INPUT_TYPE], status=row[STATUS]) \
                        .set(row[OUTPUT_BYTES])
