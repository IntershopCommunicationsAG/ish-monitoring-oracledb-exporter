from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.redo import Redo, COUNT
from tests.helpers import setUpApp, with_context


class TestRedo(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {COUNT: 100}

        redo = Redo(CollectorRegistry())

        redo.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(redo.metric.collect())).samples

        self.assertEqual(test_data[COUNT], next(iter(samples)).value)
