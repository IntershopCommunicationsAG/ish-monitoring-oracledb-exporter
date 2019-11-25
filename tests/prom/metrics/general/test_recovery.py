from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.recovery import Recovery, PERCENT_SPACE_USED, PERCENT_SPACE_RECLAIMABLE


class TestRecovery(TestCase):
    def test_should_collect(self):
        test_data_1 = {PERCENT_SPACE_USED: 100, PERCENT_SPACE_RECLAIMABLE: 234}

        recovery = Recovery(CollectorRegistry())

        recovery.collect(rows=(_ for _ in [test_data_1]))

        samples = next(iter(recovery.percent_space_used_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, PERCENT_SPACE_USED)

        samples = next(iter(recovery.percent_space_reclaimable_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, PERCENT_SPACE_RECLAIMABLE)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
