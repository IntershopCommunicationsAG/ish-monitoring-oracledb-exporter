"""Initialize prom"""

from prometheus_client import Gauge
from prometheus_client.registry import CollectorRegistry

from app.prom.collector import Collector
from app.prom.metrics.abstract_metric import AbstractMetric
from app.prom.database import util as db_util

from cx_Oracle import InterfaceError


class PromInitializer:
    """
    Initialize prom that should be used during app creation and shared in flask context(current_app)
    """

    def __init__(self, app):
        self.registry = CollectorRegistry()

        self.metrics = [
            obj(self.registry) for obj in AbstractMetric.__subclasses__()
        ]

        assert len(
            self.metrics) != 0, "At least one metric should be initialized"

        self.collector = Collector(self.metrics)
