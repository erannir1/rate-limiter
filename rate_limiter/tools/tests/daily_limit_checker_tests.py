import unittest
from unittest.mock import MagicMock

from rate_limiter.tools.daily_limit_checker import DailyLimitChecker


class TestDailyLimitChecker(unittest.TestCase):
    @classmethod
    def setUp(cls):
        # Set up a mock Redis client
        cls.mock_redis_client = MagicMock()

    @classmethod
    def tearDownClass(cls):
        # Clean up the Redis client
        cls.mock_redis_client.close()

    def test_run_tool_returns_false_when_daily_count_below_limit(self):
        # Arrange
        client_id = "client1"
        daily_limit = 5
        daily_count = 3

        self.mock_redis_client.get.return_value = str(daily_count).encode()

        checker = DailyLimitChecker(self.mock_redis_client)

        # Act
        result = checker.run_tool(client_id, daily_limit)

        # Assert
        self.assertFalse(result)
        self.mock_redis_client.get.assert_called_once_with(
            f"{client_id}:daily_count:2023-06-24"
        )
        self.mock_redis_client.set.assert_called_once_with(
            f"{client_id}:daily_count:2023-06-24", daily_count + 1
        )

    def test_run_tool_returns_true_when_daily_count_exceeds_limit(self):
        # Arrange
        client_id = "client2"
        daily_limit = 5
        daily_count = 6

        self.mock_redis_client.get.return_value = str(daily_count).encode()

        checker = DailyLimitChecker(self.mock_redis_client)

        # Act
        result = checker.run_tool(client_id, daily_limit)

        # Assert
        self.assertTrue(result)
        self.mock_redis_client.get.assert_called_once_with(
            f"{client_id}:daily_count:2023-06-24"
        )
        self.mock_redis_client.set.assert_called_once_with(
            f"{client_id}:daily_count:2023-06-24", daily_count + 1
        )

    def test_run_tool_handles_initial_daily_count(self):
        # Arrange
        client_id = "client3"
        daily_limit = 5
        initial_count = None

        self.mock_redis_client.get.return_value = initial_count

        checker = DailyLimitChecker(self.mock_redis_client)

        # Act
        result = checker.run_tool(client_id, daily_limit)

        # Assert
        self.assertFalse(result)
        self.mock_redis_client.get.assert_called_once_with(
            f"{client_id}:daily_count:2023-06-24"
        )
        self.mock_redis_client.set.assert_called_once_with(
            f"{client_id}:daily_count:2023-06-24", 1
        )


if __name__ == "__main__":
    unittest.main()
