import unittest
from unittest.mock import MagicMock, mock_open, patch

from pymongo.collection import Collection

from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants
from rate_limiter.tools.clients_collection_initializer import (
    ClientsCollectionInitializer,
)


class TestClientsCollectionInitializer(unittest.TestCase):
    def setUp(self):
        # Set up a mock clients collection
        self.mock_collection = MagicMock(spec=Collection)
        self.initializer = ClientsCollectionInitializer(self.mock_collection)

    @patch("builtins.open", mock_open(read_data='{"1111-2222-3333": {"plan": "free"}}'))
    @patch(
        "rate_limiter.tools.clients_collection_initializer.accounts",
        {"1111-2222-3333": {"plan": "free"}},
    )
    def test_run_tool_inserts_default_clients_plans(self):
        # Arrange
        self.mock_collection.count_documents.return_value = 0

        expected_documents = [
            {
                RateLimiterConstants.CLIENT_ID: "1111-2222-3333",
                RateLimiterConstants.PLAN: "free",
            }
        ]

        # Act
        self.initializer.run_tool()

        # Assert
        self.mock_collection.insert_many.assert_called_once_with(expected_documents)

    def test_run_tool_does_not_insert_documents_when_collection_not_empty(self):
        # Arrange
        self.mock_collection.count_documents.return_value = 1

        # Act
        self.initializer.run_tool()

        # Assert
        self.mock_collection.insert_many.assert_not_called()


if __name__ == "__main__":
    unittest.main()
