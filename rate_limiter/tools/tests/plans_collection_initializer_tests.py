import unittest
from unittest.mock import MagicMock

from rate_limiter.tools.plans_collection_initializer import PlansCollectionInitializer
from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants


class PlansCollectionInitializerTests(unittest.TestCase):
    def setUp(self):
        self.plans_collection = MagicMock()
        self.initializer = PlansCollectionInitializer(self.plans_collection)

    def test_run_tool_with_empty_collection(self):
        self.plans_collection.count_documents.return_value = 0

        self.initializer.run_tool()

        expected_plans = [
            {
                RateLimiterConstants.PLAN_ID: "enterprise",
                RateLimiterConstants.REQUESTS_PER_SECOND: 100,
                RateLimiterConstants.TOTAL_REQUESTS_PER_DAY: 0,
            },
            {
                RateLimiterConstants.PLAN_ID: "pro",
                RateLimiterConstants.REQUESTS_PER_SECOND: 10,
                RateLimiterConstants.TOTAL_REQUESTS_PER_DAY: 12000,
            },
            {
                RateLimiterConstants.PLAN_ID: "free",
                RateLimiterConstants.REQUESTS_PER_SECOND: 1,
                RateLimiterConstants.TOTAL_REQUESTS_PER_DAY: 50,
            },
        ]

        self.plans_collection.insert_many.assert_called_once_with(expected_plans)

    def test_run_tool_with_existing_documents(self):
        self.plans_collection.count_documents.return_value = 3

        self.initializer.run_tool()

        self.plans_collection.insert_many.assert_not_called()


if __name__ == "__main__":
    unittest.main()
