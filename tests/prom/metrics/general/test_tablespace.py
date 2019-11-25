from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.tablespace import Tablespace, TABLESPACE, TYPE, BYTES, MAX_BYTES, FREE_BYTES


class TestTablespace(TestCase):
    def test_should_collect(self):
        test_data_1 = {TABLESPACE: 'test_1', TYPE: 'test_type_1', BYTES: 300, MAX_BYTES: 100, FREE_BYTES: 234}
        test_data_2 = {TABLESPACE: 'test_2', TYPE: 'test_type_1', BYTES: 3, MAX_BYTES: 1, FREE_BYTES: 1234}

        tablespace = Tablespace(CollectorRegistry())

        tablespace.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(tablespace.bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, BYTES)

        samples = next(iter(tablespace.max_bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, MAX_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, MAX_BYTES)

        samples = next(iter(tablespace.free_bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, FREE_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, FREE_BYTES)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[TABLESPACE], sample.labels[TABLESPACE])
        self.assertEqual(test_data[TYPE], sample.labels[TYPE])
