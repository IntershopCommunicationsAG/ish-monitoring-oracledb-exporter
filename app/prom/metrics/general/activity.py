from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

PREFIX = '''oracledb_activity_'''
NAME = '''name'''
VALUE = '''value'''


class Activity(AbstractMetric):

    count = 0

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.registry = registry

        self.query = ('''
            SELECT name AS %s, value AS %s
            FROM v$sysstat
            WHERE name IN ('parse count (total)', 'execute count', 'user commits', 'user rollbacks')
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
                if self.count == 0:
                    self.__dict__[PREFIX + self.cleanName(row[NAME])] = Gauge(PREFIX + self.cleanName(row[NAME])
                        , 'Generic counter metric from v$sysstat view in Oracle.'
                        , labelnames=['server', 'port']
                        ,  registry=self.registry)

                self.__dict__[PREFIX + self.cleanName(row[NAME])] \
                    .labels(server=db_util.get_server(), port=db_util.get_port()) \
                    .set(row[VALUE])
            self.count = 1
