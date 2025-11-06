import unittest
from unittest import mock
# Assuming sqlite3 for this example.
from sqlite3 import IntegrityError as sqlite_IntegrityError

# The file being tested likely has a custom exception for IntegrityError,
# so we will adapt the tests to match the actual error messages.
from sportradar_calendar.general.services import DatabaseManager, ItemServiceError

class TestDatabaseManager(unittest.TestCase):

    @mock.patch("sportradar_calendar.general.services.get_db")
    def test_add_success(self, mock_get_db):
        """
        Test that `add` executes INSERT and commits on success.
        """
        mock_db = mock.MagicMock()
        mock_get_db.return_value = mock_db
        mgr = DatabaseManager("sport")
        
        mgr.add(name="Football", country="DE")

        mock_db.execute.assert_called_once_with(
            "INSERT INTO sport (name, country) VALUES (?, ?)",
            ("Football", "DE"),
        )
        mock_db.commit.assert_called_once()

    @mock.patch("sportradar_calendar.general.services.get_db")
    def test_add_handles_nullable_field(self, mock_get_db):
        """
        Test that `add` converts an empty value to None for a nullable field.
        """
        mock_db = mock.MagicMock()
        mock_get_db.return_value = mock_db
        mgr = DatabaseManager("sport", nullable_fields=['notes'])
        
        mgr.add(name="Football", notes="")

        mock_db.execute.assert_called_once_with(
            "INSERT INTO sport (name, notes) VALUES (?, ?)",
            ("Football", None),
        )
        mock_db.commit.assert_called_once()

    @mock.patch("sportradar_calendar.general.services.get_db")
    def test_add_raises_on_required_field_empty(self, mock_get_db):
        """
        Test that `add` raises ItemServiceError for an empty required field.
        """
        mock_db = mock.MagicMock()
        mock_get_db.return_value = mock_db
        mgr = DatabaseManager("sport")

        with self.assertRaises(ItemServiceError) as ctx:
            mgr.add(name="Tennis", country="")
        
        # FIXED: Removed single quotes around 'country' to match the actual error message.
        self.assertIn("country cannot be empty", str(ctx.exception))
        mock_db.execute.assert_not_called()

    @mock.patch("sportradar_calendar.general.services.get_db")
    def test_add_raises_on_integrity_error(self, mock_get_db):
        """
        Test that a database IntegrityError is wrapped in ItemServiceError.
        """
        mock_db = mock.MagicMock()
        mock_db.execute.side_effect = sqlite_IntegrityError("duplicate")
        mock_get_db.return_value = mock_db
        mgr = DatabaseManager("sport")

        with self.assertRaises(ItemServiceError) as ctx:
            mgr.add(name="Football")

        # FIXED: Changed assertion to check for the actual error message substring.
        self.assertIn("already exists", str(ctx.exception))
        mock_db.rollback.assert_called_once()
        mock_db.commit.assert_not_called()

if __name__ == "__main__":
    unittest.main(verbosity=2)
