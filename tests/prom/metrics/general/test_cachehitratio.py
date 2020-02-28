from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.cachehitratio import CacheHitRatio, METRIC_NAME, VALUE
from tests.helpers import setUpApp, with_context


class TestCacheHitRatio(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data_1 = {METRIC_NAME: 'test_1', VALUE: 100}
        test_data_2 = {METRIC_NAME: 'test_2', VALUE: 99.995}

        cachehitratio = CacheHitRatio(CollectorRegistry())

        cachehitratio.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(cachehitratio.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, VALUE)
        self.assert_sample_metrics(iter_samples, test_data_2, VALUE)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[METRIC_NAME], sample.labels['type'])
