"""
Collect metrics
"""
import logging

from cx_Oracle import InterfaceError

from app.prom.database import util as db_util

LOGGER = logging.getLogger(__name__)


class Collector:
    def __init__(self, metrics):
        """
        :param metrics: metrics to collect
        """
        self.metrics = metrics

    def collect(self, app):
        """
        Use database connection to collect metric
        :return:
        """
        with app.app_context():
            LOGGER.info("Start collecting metrics")
            try:
                if db_util.is_port_open():
                    with db_util.get_connection() as conn:
                        for metric in self.metrics:
                            LOGGER.debug("collect %s", metric)
                            if hasattr(metric, 'query'):
                                result = db_util.get_query_result(conn, metric.query)
                                metric.collect(result)
                            else:
                                metric.collect(app)
                else:
                    for metric in self.metrics:
                        if hasattr(metric, 'is_up_metric'):
                            metric.collect(app)
            except InterfaceError as e:
                LOGGER.error("Exception when collecting metrics: %s",
                             str(e),
                             exc_info=True)
            LOGGER.info("Finish collecting metrics")
