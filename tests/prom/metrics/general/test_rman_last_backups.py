from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.rman_last_backups import RmanLastBackups, SESSION_KEY, INPUT_TYPE, STATUS, ELAPSED_SECONDS, INPUT_BYTES, OUTPUT_BYTES
from tests.helpers import setUpApp, with_context


class TestRmanLastBackups(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data_1 = {SESSION_KEY: '148', INPUT_TYPE: 'type1', STATUS: 'stopped', ELAPSED_SECONDS: 12, INPUT_BYTES: 207.01, OUTPUT_BYTES: 230}
        test_data_2 = {SESSION_KEY: '149', INPUT_TYPE: 'type2', STATUS: 'running', ELAPSED_SECONDS: 123.45, INPUT_BYTES: 1207, OUTPUT_BYTES: 230}
        test_data_3 = {SESSION_KEY: '150', INPUT_TYPE: 'type2', STATUS: 'don''t know', ELAPSED_SECONDS: None, INPUT_BYTES: 0.01, OUTPUT_BYTES: 230}

        resource = RmanLastBackups(CollectorRegistry())

        resource.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2, test_data_3]))

        samples = next(iter(resource.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, ELAPSED_SECONDS)
        self.assert_sample_metrics(iter_samples, test_data_2, ELAPSED_SECONDS)
        # FIXME: also test if no data arrives

        samples = next(iter(resource.input_bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, INPUT_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, INPUT_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_3, INPUT_BYTES)

        samples = next(iter(resource.output_bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, OUTPUT_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, OUTPUT_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_3, OUTPUT_BYTES)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)

        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[SESSION_KEY], sample.labels[SESSION_KEY])
        self.assertEqual(test_data[INPUT_TYPE], sample.labels[INPUT_TYPE])
        self.assertEqual(test_data[STATUS], sample.labels[STATUS])
