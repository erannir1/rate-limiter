import json
import unittest
from unittest.mock import MagicMock

from rate_limiter.tools.client_limit_fetcher import (
    ClientLimitFetcher,
    ClientLimitFetcherConfig,
)

from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants


class MockRedisClient:
    def __init__(self):
        self.storage = {}

    def hget(self, key, field):
        value = self.storage.get(key, {}).get(field)
        if value is not None:
            return value.encode("utf-8")  # Return value as bytes
        return value

    def hset(self, key, field, value):
        if key not in self.storage:
            self.storage[key] = {}
        self.storage[key][field] = value


class MockClientsCollection:
    def find_one(self, query, projection):
        return {RateLimiterConstants.PLAN: "basic"}


class ClientLimitFetcherTests(unittest.TestCase):
    def setUp(self):
        self.redis_client = MockRedisClient()
        self.clients_collection = MockClientsCollection()
        self.fetcher = ClientLimitFetcher(self.redis_client, self.clients_collection)

    def test_run_tool_with_limits_in_redis(self):
        client_id = "client123"
        limits = {
            RateLimiterConstants.REQUESTS_PER_SECOND: 10,
            RateLimiterConstants.TOTAL_REQUESTS_PER_DAY: 1000,
        }
        self.redis_client.hset(
            ClientLimitFetcherConfig.CLIENT_LIMITS_KEY, client_id, json.dumps(limits)
        )

        daily_limit, second_limit = self.fetcher.run_tool(client_id, {})

        self.assertEqual(daily_limit, 1000)
        self.assertEqual(second_limit, 10)

    def test_run_tool_without_limits_in_redis(self):
        client_id = "client123"
        plans_cache = {
            "basic": {
                RateLimiterConstants.REQUESTS_PER_SECOND: 5,
                RateLimiterConstants.TOTAL_REQUESTS_PER_DAY: 500,
            }
        }
        self.fetcher.clients_collection.find_one = MagicMock(
            return_value={RateLimiterConstants.PLAN: "basic"}
        )

        daily_limit, second_limit = self.fetcher.run_tool(client_id, plans_cache)

        expected_limits = json.dumps(plans_cache["basic"])
        redis_limits = self.redis_client.hget(
            ClientLimitFetcherConfig.CLIENT_LIMITS_KEY, client_id
        ).decode("utf-8")
        self.assertEqual(redis_limits, expected_limits)


if __name__ == "__main__":
    unittest.main()
