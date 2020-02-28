from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.tablespace import Tablespace, AUTOEXTENSIBLE, TABLESPACE, CURR_BYTES, USED_BYTES, MAX_BYTES, FREE_BYTES
from tests.helpers import setUpApp, with_context


class TestTablespace(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data_1 = {TABLESPACE: 'test_1', AUTOEXTENSIBLE: 'YES', CURR_BYTES: 300, USED_BYTES: 230, MAX_BYTES: 100, FREE_BYTES: 234}
        test_data_2 = {TABLESPACE: 'test_2', AUTOEXTENSIBLE: 'NO', CURR_BYTES: 3, USED_BYTES: 2, MAX_BYTES: 1, FREE_BYTES: 1234}

        tablespace = Tablespace(CollectorRegistry())

        tablespace.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(tablespace.curr_bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, CURR_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, CURR_BYTES)

        samples = next(iter(tablespace.used_bytes_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, USED_BYTES)
        self.assert_sample_metrics(iter_samples, test_data_2, USED_BYTES)

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
