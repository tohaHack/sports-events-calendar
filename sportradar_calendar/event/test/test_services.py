import unittest
from unittest import mock

from sportradar_calendar.event.services import DatabaseManagerEvent

class TestDatabaseManagerEvent(unittest.TestCase):

    def setUp(self):
        """
        Instantiate the manager before each test.
        """
        self.manager = DatabaseManagerEvent()

    @mock.patch('sportradar_calendar.event.services.get_db')
    def test_get_all_ordered(self, mock_get_db):
        """
        Test that get_all_ordered constructs the correct SQL query.
        """
        mock_connection = mock.MagicMock()
        mock_get_db.return_value = mock_connection
        expected_sql = "SELECT * FROM event ORDER BY event_date DESC"

        self.manager.get_all_ordered()

        mock_connection.execute.assert_called_once_with(expected_sql)

    @mock.patch('sportradar_calendar.event.services.get_db')
    def test_get_filtered_sql_construction(self, mock_get_db):
        """
        Test that get_filtered constructs the correct SQL and parameters
        for various filter combinations.
        """
        mock_connection = mock.MagicMock()
        mock_get_db.return_value = mock_connection

        test_cases = [
            ("No filters", {}, "SELECT * FROM event ORDER BY event_date DESC", {}),
            ("Sport ID only", {'sport_id': 1}, "SELECT * FROM event WHERE  _sport_id = :sport_id  ORDER BY event_date DESC", {'sport_id': 1}),
            ("Date From only", {'date_from': '2025-11-01'}, "SELECT * FROM event WHERE  event_date >= :date_from  ORDER BY event_date DESC", {'date_from': '2025-11-01'}),
            ("Date To without time", {'date_to': '2025-11-30'}, "SELECT * FROM event WHERE  event_date <= :date_to  ORDER BY event_date DESC", {'date_to': '2025-11-30T23:59'}),
            ("Date To with time", {'date_to': '2025-11-30T18:00'}, "SELECT * FROM event WHERE  event_date <= :date_to  ORDER BY event_date DESC", {'date_to': '2025-11-30T18:00'}),
            ("All filters", {'sport_id': 5, 'date_from': '2025-11-01', 'date_to': '2025-11-15'}, "SELECT * FROM event WHERE  _sport_id = :sport_id  AND  event_date >= :date_from  AND  event_date <= :date_to  ORDER BY event_date DESC", {'sport_id': 5, 'date_from': '2025-11-01', 'date_to': '2025-11-15T23:59'}),
        ]

        for name, kwargs, expected_sql, expected_params in test_cases:
            with self.subTest(msg=name):
                self.manager.get_filtered(**kwargs)
                mock_connection.execute.assert_called_with(expected_sql, expected_params)
                mock_connection.reset_mock()

if __name__ == '__main__':
    unittest.main()
