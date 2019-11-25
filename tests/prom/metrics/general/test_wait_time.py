from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.wait_time import WaitTime, PREFIX, WAIT_CLASS, VALUE


class TestActivity(TestCase):
    def test_should_collect(self):
        test_data_1 = {WAIT_CLASS: 'Application', VALUE: 1.23}
        test_data_2 = {WAIT_CLASS: 'User I/O', VALUE: 3}

        wait_time = WaitTime(CollectorRegistry())

        wait_time.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        self.assert_sample_metrics(wait_time, PREFIX + 'application', test_data_1)
        self.assert_sample_metrics(wait_time, PREFIX + 'user_io', test_data_2)

    def assert_sample_metrics(self, wait_time, metric_name, test_data):
        samples = next(iter(wait_time.__dict__[metric_name].collect())).samples
        iter_samples = iter(samples)
        sample = next(iter_samples)
        self.assertEqual(test_data[VALUE], sample.value)
