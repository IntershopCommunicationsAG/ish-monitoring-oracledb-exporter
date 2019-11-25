from unittest import TestCase, mock
from unittest.mock import MagicMock

from cx_Oracle import InterfaceError

from app.prom import collector


class TestCollector(TestCase):

    @mock.patch('app.prom.collector.db_util.get_query_result')
    @mock.patch('app.prom.collector.db_util.get_connection')
    def test_should_collect(self, mock_connection, mock_query_result):
        app = MagicMock()
        collector_init = collector.Collector([MagicMock(), ])
        collector_init.collect(app)

        mock_connection.assert_called_once()
        self.assertEqual(mock_query_result.call_count, len(collector_init.metrics))

    @mock.patch('app.prom.collector.db_util.get_query_result')
    @mock.patch('app.prom.collector.db_util.get_connection')
    def test_should_not_get_query_result_given_InterfaceError(self, mock_connection, mock_query_result):
        mock_connection.side_effect = InterfaceError()
        app = MagicMock()
        collector_init = collector.Collector([1, 2, 3, ])
        collector_init.collect(app)
        collector_init.collect(app)
        mock_query_result.assert_not_called()
