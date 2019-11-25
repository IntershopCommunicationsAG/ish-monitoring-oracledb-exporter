from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

NAME = '''name'''
TOTAL = '''total'''
FREE = '''free'''

class ASMDiskGroup(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.total_size_metric = Gauge('oracledb_asm_diskgroup_total',
                                      'Total size of ASM disk group.',
                                      labelnames=[NAME],
                                      registry=registry)
        self.free_space_metric = Gauge(
            'oracledb_asm_diskgroup_free',
            'Free space available on ASM disk group.',
            labelnames=[NAME],
            registry=registry)

        self.query = '''
        SELECT name AS %s, total_mb*1024*1024 AS %s, free_mb*1024*1024 AS %s
        FROM v$asm_diskgroup
        ''' % (NAME, TOTAL, FREE)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.total_size_metric \
                .labels(name=row[NAME]) \
                .set(row[TOTAL])

            self.free_space_metric \
                .labels(name=row[NAME]) \
                .set(row[FREE])

