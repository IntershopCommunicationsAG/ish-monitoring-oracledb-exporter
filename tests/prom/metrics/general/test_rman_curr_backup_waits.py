from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.rman_curr_backup_waits import RmanCurrBackupWaits, SID, CLIENT_INFO, SEQUENCE, EVENT, STATE, WAITING_TIME
from tests.helpers import setUpApp, with_context


class TestRmanCurrBackupWaits(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data_1 = {SID: '148', CLIENT_INFO: '', SEQUENCE: '8200', EVENT: 'sql_net_message_from_client', STATE: 'WAITING', WAITING_TIME: 207.01}
        test_data_2 = {SID: '149', CLIENT_INFO: '', SEQUENCE: '8200', EVENT: 'sql_net_message_from_client', STATE: 'WAITING', WAITING_TIME: 1207}
        test_data_3 = {SID: '150', CLIENT_INFO: '', SEQUENCE: '8200', EVENT: 'sql_net_message_from_client', STATE: 'WAITING', WAITING_TIME: 0.01}

        resource = RmanCurrBackupWaits(CollectorRegistry())

        resource.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2, test_data_3]))

        samples = next(iter(resource.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metrics(iter_samples, test_data_1, WAITING_TIME)
        self.assert_sample_metrics(iter_samples, test_data_2, WAITING_TIME)
        self.assert_sample_metrics(iter_samples, test_data_3, WAITING_TIME)

    def assert_sample_metrics(self, iter_samples, test_data, value_name):
        sample = next(iter_samples)
        self.assertEqual(test_data[value_name], sample.value)
        self.assertEqual(test_data[SID], sample.labels[SID])
        self.assertEqual(test_data[CLIENT_INFO], sample.labels[CLIENT_INFO])
        self.assertEqual(test_data[SEQUENCE], sample.labels[SEQUENCE])
        self.assertEqual(test_data[EVENT], sample.labels[EVENT])
        self.assertEqual(test_data[STATE], sample.labels[STATE])
