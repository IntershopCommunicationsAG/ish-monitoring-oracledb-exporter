from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.process import Process, COUNT


class TestProcess(TestCase):
    def test_should_collect(self):
        test_data = {COUNT: 100}

        process = Process(CollectorRegistry())

        process.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(process.metric.collect())).samples

        self.assertEqual(test_data[COUNT], next(iter(samples)).value)
