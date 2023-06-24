import json

from pymongo.collection import Collection

from rate_limiter.types.plan import Plan
from rate_limiter.types.client_doc import ClientDoc
from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants


class ClientLimitFetcherConfig:
    CLIENT_LIMITS_KEY = "clients_limits"


class ClientLimitFetcher:
    def __init__(self, redis_client, clients_collection: Collection):
        self.class_config = ClientLimitFetcherConfig
        self.redis_client = redis_client
        self.clients_collection: Collection = clients_collection

    def run_tool(self, client_id, plans_cache):
        limits = self.redis_client.hget(self.class_config.CLIENT_LIMITS_KEY, client_id)
        if not limits:
            limits: Plan = self.handle_no_limits(client_id, plans_cache)
        else:
            limits: Plan = json.loads(
                limits.decode("utf-8")
            )  # Convert limits bytes to dictionary

        second_limit: int = int(limits.get(RateLimiterConstants.REQUESTS_PER_SECOND, 0))
        daily_limit: int = int(
            limits.get(RateLimiterConstants.TOTAL_REQUESTS_PER_DAY, 0)
        )
        return daily_limit, second_limit

    def handle_no_limits(self, client_id, plans_cache) -> Plan:
        client_doc: ClientDoc = self.clients_collection.find_one(
            {RateLimiterConstants.CLIENT_ID: client_id}, {"_id": 0}
        )  # Exclude the _id field from the query projection
        client_plan: str = client_doc[RateLimiterConstants.PLAN]
        limits: Plan = plans_cache[client_plan]
        self.redis_client.hset(
            self.class_config.CLIENT_LIMITS_KEY, client_id, json.dumps(limits)
        )
        return limits
