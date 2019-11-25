from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.asm_diskgroup import ASMDiskGroup, NAME, TOTAL, FREE


class TestASMDiskGroup(TestCase):
    def test_should_collect(self):
        test_data_1 = {NAME: 'test_1', TOTAL: 300, FREE: 100}
        test_data_2 = {NAME: 'test_2', TOTAL: 3, FREE: 1}

        asm_diskgroup = ASMDiskGroup(CollectorRegistry())

        asm_diskgroup.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(asm_diskgroup.total_size_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, TOTAL)
        self.assert_sample_metrics(iter_samples, test_data_2, TOTAL)

        samples = next(iter(asm_diskgroup.free_space_metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, FREE)
        self.assert_sample_metrics(iter_samples, test_data_2, FREE)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[NAME], sample.labels[NAME])
