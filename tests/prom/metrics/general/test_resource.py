from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.resource import Resource, NAME, CURRENT_UTILIZATION, LIMIT_VALUE
from tests.helpers import setUpApp, with_context


class TestResource(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data_1 = {NAME: 'test_1', CURRENT_UTILIZATION: 300, LIMIT_VALUE: 100}
        test_data_2 = {NAME: 'test_2', CURRENT_UTILIZATION: 3, LIMIT_VALUE: 1}
        test_data_3 = {NAME: 'test_3', CURRENT_UTILIZATION: 0, LIMIT_VALUE: 'UNLIMITED'}

        resource = Resource(CollectorRegistry())

        resource.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2, test_data_3]))

        samples = next(iter(resource.current_utilization_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, CURRENT_UTILIZATION)
        self.assert_sample_metrics(iter_samples, test_data_2, CURRENT_UTILIZATION)
        self.assert_sample_metrics(iter_samples, test_data_3, CURRENT_UTILIZATION)

        samples = next(iter(resource.limit_value_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, LIMIT_VALUE)
        self.assert_sample_metrics(iter_samples, test_data_2, LIMIT_VALUE)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[NAME], sample.labels[NAME])
