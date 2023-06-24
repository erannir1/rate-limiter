import unittest
from unittest.mock import MagicMock

from pymongo.collection import Collection

from rate_limiter.tools.plans_fetcher import PlansFetcher


class TestPlansFetcher(unittest.TestCase):
    def setUp(self):
        # Set up a mock plans collection
        self.mock_plans_collection = MagicMock(spec=Collection)

    def test_run_tool_returns_empty_dict_when_no_plans(self):
        # Arrange
        self.mock_plans_collection.find.return_value = []

        fetcher = PlansFetcher(self.mock_plans_collection)

        # Act
        result = fetcher.run_tool()

        # Assert
        self.assertEqual(result, {})

    def test_run_tool_returns_plans_dict_when_plans_exist(self):
        # Arrange
        plans = [
            {
                "plan_id": "free",
                "requests_per_second": 10,
                "total_requests_per_day": 1000,
            },
            {
                "plan_id": "pro",
                "requests_per_second": 20,
                "total_requests_per_day": 2000,
            },
        ]

        self.mock_plans_collection.find.return_value = plans

        fetcher = PlansFetcher(self.mock_plans_collection)

        # Act
        result = fetcher.run_tool()

        # Assert
        expected_result = {
            "free": {
                "plan_id": "free",
                "requests_per_second": 10,
                "total_requests_per_day": 1000,
            },
            "pro": {
                "plan_id": "pro",
                "requests_per_second": 20,
                "total_requests_per_day": 2000,
            },
        }
        self.assertEqual(result, expected_result)

    def tearDown(self):
        # Additional cleanup if needed
        pass


if __name__ == "__main__":
    unittest.main()
