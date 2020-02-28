from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.sessions import Sessions, SESSIONS_STATUS, SESSIONS_TYPE, SESSIONS_COUNT
from tests.helpers import setUpApp, with_context


class TestConnection(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        sessions = Sessions(CollectorRegistry())
        test_data_1 = {SESSIONS_STATUS: 'ACTIVE', SESSIONS_TYPE: 'user', SESSIONS_COUNT: 50}
        test_data_2 = {SESSIONS_STATUS: 'INACTIVE', SESSIONS_TYPE: 'background', SESSIONS_COUNT: 2}

        sessions.collect(self.app, rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(sessions.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample(iter_samples, test_data_1)
        self.assert_sample(iter_samples, test_data_2)

    def assert_sample(self, iter_samples, test_data):
        sample = next(iter_samples)
        self.assertEqual(test_data[SESSIONS_COUNT], sample.value)
        self.assertEqual(test_data[SESSIONS_STATUS], sample.labels[SESSIONS_STATUS])
        self.assertEqual(test_data[SESSIONS_TYPE], sample.labels[SESSIONS_TYPE])
