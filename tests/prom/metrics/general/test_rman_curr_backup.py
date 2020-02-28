from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.rman_curr_backup import RmanCurrBackup, SID, CONTEXT, TIME_REMAINING, SOFAR, TOTALWORK
from tests.helpers import setUpApp, with_context


class TestRmanCurrBackup(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data_1 = {SID: '148', CONTEXT: '1', TIME_REMAINING: 12, SOFAR: 12, TOTALWORK: 207.01}
        test_data_2 = {SID: '149', CONTEXT: '2', TIME_REMAINING: 1, SOFAR: 123.45, TOTALWORK: 1207}
        test_data_3 = {SID: '150', CONTEXT: '3', TIME_REMAINING: 23.34, SOFAR: 13, TOTALWORK: 0.01}

        resource = RmanCurrBackup(CollectorRegistry())

        resource.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2, test_data_3]))

        samples = next(iter(resource.time_remaining_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, TIME_REMAINING)
        self.assert_sample_metrics(iter_samples, test_data_2, TIME_REMAINING)
        self.assert_sample_metrics(iter_samples, test_data_3, TIME_REMAINING)

        samples = next(iter(resource.sofar_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, SOFAR)
        self.assert_sample_metrics(iter_samples, test_data_2, SOFAR)
        self.assert_sample_metrics(iter_samples, test_data_3, SOFAR)

        samples = next(iter(resource.total_work_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, TOTALWORK)
        self.assert_sample_metrics(iter_samples, test_data_2, TOTALWORK)
        self.assert_sample_metrics(iter_samples, test_data_3, TOTALWORK)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[SID], sample.labels[SID])
        self.assertEqual(test_data[CONTEXT], sample.labels[CONTEXT])
