from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

PERCENT_SPACE_USED = '''percent_space_used'''
PERCENT_SPACE_RECLAIMABLE = '''percent_space_reclaimable'''


class Recovery(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.percent_space_used_metric = Gauge('oracledb_recovery_percent_space_used',
                                  'Generic counter metric of tablespaces bytes in Oracle.',
                                  registry=registry)

        self.percent_space_reclaimable_metric = Gauge('oracledb_recovery_percent_space_reclaimable',
                                  'Generic counter metric of tablespaces bytes in Oracle.',
                                  registry=registry)


        self.query = '''
        SELECT sum(percent_space_used) AS %s , sum(percent_space_reclaimable) AS %s
        FROM V$FLASH_RECOVERY_AREA_USAGE
        ''' % (PERCENT_SPACE_USED, PERCENT_SPACE_RECLAIMABLE)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            if row[PERCENT_SPACE_USED] is not None:
                self.percent_space_used_metric \
                    .set(row[PERCENT_SPACE_USED])

            if row[PERCENT_SPACE_RECLAIMABLE] is not None:
                self.percent_space_reclaimable_metric \
                    .set(row[PERCENT_SPACE_RECLAIMABLE])
