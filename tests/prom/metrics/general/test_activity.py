from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.activity import Activity, PREFIX, NAME, VALUE


class TestActivity(TestCase):
    def test_should_collect(self):
        test_data_1 = {NAME: 'user commits', VALUE: 300}
        test_data_2 = {NAME: 'parse count (total)', VALUE: 3}

        activity = Activity(CollectorRegistry())

        activity.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        self.assert_sample_metrics(activity, PREFIX + 'user_commits', test_data_1)
        self.assert_sample_metrics(activity, PREFIX + 'parse_count_total', test_data_2)

    def assert_sample_metrics(self, resource, metric_name, test_data):
        samples = next(iter(resource.__dict__[metric_name].collect())).samples
        iter_samples = iter(samples)
        sample = next(iter_samples)
        self.assertEqual(test_data[VALUE], sample.value)
