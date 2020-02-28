from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

PREFIX = '''oracledb_wait_time_'''
WAIT_CLASS = '''wait_class'''
VALUE = '''value'''


class WaitTime(AbstractMetric):

    count = 0

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.registry = registry

        self.query = ('''
            SELECT
              n.wait_class as %s,
              round(m.time_waited/m.INTSIZE_CSEC,3) as %s
            FROM
              v$waitclassmetric  m, v$system_wait_class n
            WHERE
              m.wait_class_id=n.wait_class_id AND n.wait_class != 'Idle'
        ''' % (WAIT_CLASS, VALUE))

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:

                if self.count == 0:
                    self.__dict__[PREFIX + self.cleanName(row[WAIT_CLASS])] = Gauge(PREFIX + self.cleanName(row[WAIT_CLASS])
                        , 'Generic counter metric from v$waitclassmetric view in Oracle.'
                        , labelnames=['server', 'port']
                        , registry=self.registry)

                self.__dict__[PREFIX + self.cleanName(row[WAIT_CLASS])] \
                    .labels(server=db_util.get_server(), port=db_util.get_port()) \
                    .set(row[VALUE])
            self.count = 1
