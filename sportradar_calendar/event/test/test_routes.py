import unittest
from unittest import mock
from flask import Flask
from datetime import datetime

# We assume tests are executed in a context where sportradar_calendar is a package.
# This allows direct import of the module under test.
from sportradar_calendar.event import routes

class TestEventRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a Flask app context for the test suite."""
        cls.app = Flask(__name__)
        cls.app.secret_key = "dev"


    @mock.patch("sportradar_calendar.event.routes.render_template")
    @mock.patch("sportradar_calendar.event.routes.venue_manager")
    @mock.patch("sportradar_calendar.event.routes.team_manager")
    @mock.patch("sportradar_calendar.event.routes.sport_manager")
    @mock.patch("sportradar_calendar.event.routes.manager")
    def test_add_view_get(self, mock_manager, mock_sport_manager, mock_team_manager, mock_venue_manager, mock_render_template):
        """
        Test `add_view` for a GET request.
        It should fetch data from all managers and render the add form template.
        """
        # Arrange
        mock_sport_manager.get_all.return_value = [{"sport_id": 1, "name": "Test Sport"}]
        mock_team_manager.get_all.return_value = [{"team_id": 1, "name": "Test Team"}]
        mock_venue_manager.get_all.return_value = [{"venue_id": 1, "name": "Test Venue", "city": "Test City"}]
        mock_manager.get_columns.return_value = ["event_date", "_sport_id"]
        
        with self.app.test_request_context(method="GET"):
            # Act
            routes.add_view()

            # Assert
            mock_sport_manager.get_all.assert_called_once()
            mock_team_manager.get_all.assert_called_once()
            mock_venue_manager.get_all.assert_called_once()
            mock_manager.get_columns.assert_called_once()
            
            mock_render_template.assert_called_once_with(
                "event/form_add_event.html",
                columns=["event_date", "_sport_id"],
                sports=[{"sport_id": 1, "name": "Test Sport"}],
                teams=[{"team_id": 1, "name": "Test Team"}],
                venues=[{"venue_id": 1, "name": "Test Venue", "city": "Test City"}],
            )

    @mock.patch("sportradar_calendar.event.routes.general_add_view")
    @mock.patch("sportradar_calendar.event.routes.manager")
    def test_add_view_post(self, mock_manager, mock_general_add_view):
        """
        Test `add_view` for a POST request.
        It should delegate add logic to general_add_view.
        """
        with self.app.test_request_context(method="POST", data={"event_date": "2025-01-01T12:00"}):
            # Act
            routes.add_view()

            # Assert
            mock_general_add_view.assert_called_once_with(
                manager=mock_manager, endpoint="event/form_add_event.html"
            )

    @mock.patch("sportradar_calendar.event.routes.general_get_all_view")
    @mock.patch("sportradar_calendar.event.routes.venue_manager")
    @mock.patch("sportradar_calendar.event.routes.team_manager")
    @mock.patch("sportradar_calendar.event.routes.sport_manager")
    @mock.patch("sportradar_calendar.event.routes.manager")
    def test_get_all_view_with_filters(self, mock_manager, mock_sport_manager, mock_team_manager, mock_venue_manager, mock_general_get_all_view):
        """
        Test `get_all_view` with filtering parameters.
        It should handle lookups, format dates and call the general view.
        """
        # Arrange
        mock_events = [{"event_id": 1, "event_date": "2025-11-20T18:00", "_sport_id": 1, "_home_team_id": 1, "_away_team_id": 2, "_venue_id": 1}]
        mock_manager.get_filtered.return_value = mock_events
        
        mock_sports = [{"sport_id": 1, "name": "Football"}]
        mock_sport_manager.get_all.return_value = mock_sports
        
        mock_teams = [{"team_id": 1, "name": "Team A"}, {"team_id": 2, "name": "Team B"}]
        mock_team_manager.get_all.return_value = mock_teams
        
        mock_venues = [{"venue_id": 1, "name": "Venue 1", "city": "City 1"}]
        mock_venue_manager.get_all.return_value = mock_venues

        query_string = "sport_id=1&date_from=2025-11-01&date_to=2025-11-30"
        with self.app.test_request_context(method="GET", query_string=query_string):
            # Act
            routes.get_all_view()

            # Assert
            mock_manager.get_filtered.assert_called_once_with(sport_id=1, date_from='2025-11-01', date_to='2025-11-30')

            expected_items = [
                {
                    "event_id": 1,
                    "event_date": "2025-11-20T18:00",
                    "event_date_fmt": "2025-11-20 18:00",
                    "_sport_id": 1,
                    "_home_team_id": 1,
                    "_away_team_id": 2,
                    "_venue_id": 1,
                }
            ]
            
            _, kwargs = mock_general_get_all_view.call_args
            self.assertEqual(kwargs['items'], expected_items)
            self.assertEqual(kwargs['selected_sport'], 1)
            self.assertEqual(kwargs['date_from'], '2025-11-01')
            self.assertEqual(kwargs['date_to'], '2025-11-30')
            self.assertIn("_sport_id", kwargs['lookups'])
            self.assertEqual(kwargs['lookups']['_sport_id'], {1: 'Football'})


    @mock.patch("sportradar_calendar.event.routes.general_delete")
    @mock.patch("sportradar_calendar.event.routes.manager")
    def test_delete(self, mock_manager, mock_general_delete):
        """
        Test the `delete` function.
        It should delegate deletion logic to the general_delete helper.
        """
        # Act
        routes.delete(id=42)

        # Assert
        mock_general_delete.assert_called_once_with(
            manager=mock_manager, id=42, endpoint="event/index.html"
        )

if __name__ == '__main__':
    unittest.main()