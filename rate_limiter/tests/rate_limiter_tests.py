import unittest
from unittest.mock import MagicMock

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from rate_limiter.rate_limiter import RateLimiter


class MockRedisClient:
    def __init__(self):
        self.counter = {}

    def incr(self, key, amount=1):
        self.counter[key] = self.counter.get(key, 0) + amount
        return self.counter[key]

    def get(self, key):
        return self.counter.get(key)


class RateLimiterTests(unittest.TestCase):
    def setUp(self):
        # Mock MongoDB and Redis clients
        self.mongo_client = MagicMock(MongoClient)
        self.redis_client = MockRedisClient()

        # Mock MongoDB collections
        self.plans_collection = MagicMock(Collection)
        self.clients_collection = MagicMock(Collection)
        self.db = MagicMock(Database)
        self.db.__getitem__.side_effect = (
            lambda name: self.plans_collection
            if name == "plans"
            else self.clients_collection
        )
        self.mongo_client.__getitem__.return_value = self.db

        # Create RateLimiter instance
        self.rate_limiter = RateLimiter(
            mongo_client=self.mongo_client, redis_client=self.redis_client
        )

    def test_limit_exceeded_below_limits(self):
        # Mock client limit fetcher
        self.rate_limiter.client_limit_fetcher.run_tool = MagicMock(
            return_value=(1000, 10)
        )

        # Mock requests per second counter
        self.rate_limiter.requests_per_second_counter.run_tool = MagicMock(
            return_value=5
        )

        # Mock daily limit checker
        self.rate_limiter.daily_limit_checker.run_tool = MagicMock(return_value=False)

        # Test limit_exceeded method
        self.assertFalse(self.rate_limiter.limit_exceeded("client1"))

    def test_limit_exceeded_above_secondly_limit(self):
        self.rate_limiter.client_limit_fetcher.run_tool = MagicMock(
            return_value=(1000, 10)
        )
        self.rate_limiter.requests_per_second_counter.run_tool = MagicMock(
            return_value=15
        )
        self.rate_limiter.daily_limit_checker.run_tool = MagicMock(return_value=False)

        self.assertTrue(self.rate_limiter.limit_exceeded("client2"))

    def test_limit_exceeded_above_daily_limit(self):
        self.rate_limiter.client_limit_fetcher.run_tool = MagicMock(
            return_value=(1000, 10)
        )
        self.rate_limiter.requests_per_second_counter.run_tool = MagicMock(
            return_value=5
        )
        self.rate_limiter.daily_limit_checker.run_tool = MagicMock(return_value=True)

        self.assertTrue(self.rate_limiter.limit_exceeded("client3"))


if __name__ == "__main__":
    unittest.main()
