import logging
from unittest import TestCase
from unittest.mock import MagicMock

from cx_Oracle import DatabaseError

from app.prom.database.util import get_query_result


class TestUtil(TestCase):

    def test_should_get_query_result(self):
        test_input = [1, 2, 3]
        cursor_context = MagicMock()
        cursor_context.__iter__.return_value = test_input

        cursor = MagicMock()
        cursor.__enter__.return_value = cursor_context

        connection = MagicMock()
        connection.cursor.return_value = cursor

        for row in get_query_result(connection, 'test'):
            self.assertTrue(row in test_input)

    def test_should_raise_nothing_DatabaseError(self):
        cursor_context = MagicMock()
        cursor_context.execute.side_effect = DatabaseError("Test")

        cursor = MagicMock()
        cursor.__enter__.return_value = cursor_context

        connection = MagicMock()
        connection.cursor.return_value = cursor

        for row in get_query_result(connection, 'test'):
            logging.info(row)
