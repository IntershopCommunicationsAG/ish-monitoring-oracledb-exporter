from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

TABLESPACE = '''tablespace'''
TYPE = '''type'''
CURR_BYTES = '''curr_bytes'''
USED_BYTES = '''used_bytes'''
MAX_BYTES = '''max_bytes'''
FREE_BYTES = '''free'''
AUTOEXTENSIBLE = '''autoextensible'''

class Tablespace(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.curr_bytes_metric = Gauge('oracledb_tablespace_curr_bytes'
            , 'Generic counter metric of tablespaces current bytes in Oracle.'
            , labelnames=['server', 'port', TABLESPACE]
            , registry=registry)

        self.used_bytes_metric = Gauge('oracledb_tablespace_used_bytes'
            , 'Generic counter metric of tablespaces used bytes in Oracle.'
            , labelnames=['server', 'port', TABLESPACE]
            , registry=registry)

        self.max_bytes_metric = Gauge('oracledb_tablespace_max_bytes'
            , 'Generic counter metric of tablespaces max bytes in Oracle.'
            , labelnames=['server', 'port', TABLESPACE, AUTOEXTENSIBLE]
            , registry=registry)

        self.free_bytes_metric = Gauge('oracledb_tablespace_free'
            , 'Generic counter metric of tablespaces free bytes in Oracle.'
            , labelnames=['server', 'port', TABLESPACE]
            , registry=registry)

        self.query = '''
            SELECT df.tablespace_name AS %s,
                   Round(df.maxbytes, 2) AS %s,
                   Round(df.bytes, 2) AS %s,
                   Round((df.bytes - SUM(fs.bytes)), 2) AS %s,
                   Round(SUM(fs.bytes), 2) AS %s,
                   Max(autoextensible) AS %s
            FROM   dba_free_space fs,
                   (SELECT tablespace_name,
                           SUM(bytes)                      bytes,
                           SUM(Decode(maxbytes, 0, bytes,
                                                maxbytes)) maxbytes,
                           Max(autoextensible)             autoextensible
                    FROM   dba_data_files
                    GROUP  BY tablespace_name) df
            WHERE  fs.tablespace_name (+) = df.tablespace_name
            GROUP  BY df.tablespace_name,
                      df.bytes,
                      df.maxbytes
            UNION ALL
            SELECT df.tablespace_name AS %s,
                   Round(df.maxbytes, 2) AS %s,
                   Round(df.bytes, 2) AS %s,
                   Round((df.bytes - SUM(fs.bytes)), 2) AS %s,
                   Round(SUM(fs.bytes), 2) AS %s,
                   Max(autoextensible) AS %s
            FROM   (SELECT tablespace_name,
                           bytes_used bytes
                    FROM   v$temp_space_header
                    GROUP  BY tablespace_name,
                              bytes_free,
                              bytes_used) fs,
                   (SELECT tablespace_name,
                           SUM(bytes)                      bytes,
                           SUM(Decode(maxbytes, 0, bytes,
                                                maxbytes)) maxbytes,
                           Max(autoextensible)             autoextensible
                    FROM   dba_temp_files
                    GROUP  BY tablespace_name) df
            WHERE  fs.tablespace_name (+) = df.tablespace_name
            GROUP  BY df.tablespace_name,
                      df.bytes,
                      df.maxbytes
        ''' % (TABLESPACE, MAX_BYTES, CURR_BYTES, USED_BYTES, FREE_BYTES, AUTOEXTENSIBLE, TABLESPACE, MAX_BYTES, CURR_BYTES, USED_BYTES, FREE_BYTES, AUTOEXTENSIBLE)

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                self.curr_bytes_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), tablespace=row[TABLESPACE]) \
                    .set(row[CURR_BYTES])

                self.used_bytes_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), tablespace=row[TABLESPACE]) \
                    .set(row[USED_BYTES])

                self.max_bytes_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), tablespace=row[TABLESPACE], autoextensible=row[AUTOEXTENSIBLE]) \
                    .set(row[MAX_BYTES])

                self.free_bytes_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), tablespace=row[TABLESPACE]) \
                    .set(row[FREE_BYTES])
