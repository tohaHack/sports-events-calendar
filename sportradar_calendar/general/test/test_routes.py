import unittest
from unittest import mock
from flask import Flask

# Import the module to be tested and its dependencies
from sportradar_calendar.general import routes
from sportradar_calendar.general.services import DatabaseManager, ItemServiceError

class TestGeneralRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up a Flask application context for the test suite.
        This provides the necessary context for functions that use `request`.
        """
        cls.app = Flask(__name__)
        cls.app.secret_key = "dev" # Required for flash messages

    @mock.patch("sportradar_calendar.general.routes.render_template")
    @mock.patch("sportradar_calendar.general.routes.flash")
    def test_general_add_view_post_success(self, mock_flash, mock_render_template):
        """
        Test the successful addition of an item via a POST request.
        """
        # Arrange: Create a mock manager and define the endpoint
        mock_manager = mock.MagicMock(spec=DatabaseManager)
        mock_manager.get_columns.return_value = []
        endpoint = "sport/form_add_sport.html"
        
        # Use the app context to simulate a POST request
        with self.app.test_request_context(method="POST", data={"name": "Test Sport"}):
            # Act: Call the view function
            routes.general_add_view(manager=mock_manager, endpoint=endpoint)

            # Assert: Check that the manager's add method was called and a success flash was sent
            mock_manager.add.assert_called_once_with(name="Test Sport")
            mock_flash.assert_called_once_with("Item is successfully added!", "success")
            mock_render_template.assert_called_once_with(endpoint, columns=[])

    @mock.patch("sportradar_calendar.general.routes.render_template")
    @mock.patch("sportradar_calendar.general.routes.flash")
    def test_general_add_view_post_failure(self, mock_flash, mock_render_template):
        """
        Test the failed addition of an item when the manager raises an ItemServiceError.
        """
        # Arrange: Set up a manager that raises an error on `add`
        mock_manager = mock.MagicMock(spec=DatabaseManager)
        mock_manager.get_columns.return_value = []
        error = ItemServiceError("Add failed")
        mock_manager.add.side_effect = error
        endpoint = "sport/form_add_sport.html"

        with self.app.test_request_context(method="POST", data={"name": "Test Sport"}):
            # Act
            routes.general_add_view(manager=mock_manager, endpoint=endpoint)

            # Assert: Check that a danger flash message was shown with the error
            mock_manager.add.assert_called_once_with(name="Test Sport")
            mock_flash.assert_called_once_with(str(error), "danger")
            mock_render_template.assert_called_once_with(endpoint, columns=[])

    @mock.patch("sportradar_calendar.general.routes.render_template")
    def test_general_get_all_view(self, mock_render_template):
        """
        Test that fetching and displaying all items works correctly.
        """
        # Arrange
        mock_manager = mock.MagicMock(spec=DatabaseManager)
        mock_items = [{"sport_id": 1, "name": "Test Sport"}]
        mock_columns = [{"name": "sport_id"}, {"name": "name"}]
        mock_manager.get_all.return_value = mock_items
        mock_manager.get_columns.return_value = mock_columns
        endpoint = "sport/index.html"

        with self.app.test_request_context(method="GET"):
            # Act
            routes.general_get_all_view(manager=mock_manager, endpoint=endpoint)

            # Assert: Check that the correct template and context were used
            mock_manager.get_all.assert_called_once()
            mock_manager.get_columns.assert_called_once()
            mock_render_template.assert_called_once_with(
                endpoint,
                manager=mock_manager,
                items=mock_items,
                columns=mock_columns,
                id_field="sport_id",
                lookups=None,
                header_labels=None,
            )

    @mock.patch("sportradar_calendar.general.routes.general_get_all_view")
    @mock.patch("sportradar_calendar.general.routes.flash")
    def test_general_delete_success(self, mock_flash, mock_get_all_view):
        """
        Test the successful deletion of an item.
        It should call the manager's delete method and then re-render the list view.
        """
        # Arrange
        mock_manager = mock.MagicMock(spec=DatabaseManager)
        
        with self.app.test_request_context():
            # Act: Call the delete function
            routes.general_delete(manager=mock_manager, id=1, endpoint="sport.index")
        
        # Assert: Check that delete was called and a flash message was sent
        mock_manager.delete.assert_called_once_with(id=1)
        mock_flash.assert_called_once_with('Item "1" deleted', "success")
        
        # Assert that the list view function is called to re-render the page
        mock_get_all_view.assert_called_once_with(manager=mock_manager, endpoint="sport.index")


if __name__ == '__main__':
    unittest.main(verbosity=2)
