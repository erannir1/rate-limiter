from typing import Dict

import redis
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from rate_limiter.types.plan import Plan
from rate_limiter.tools.plans_fetcher import PlansFetcher
from rate_limiter.tools.daily_limit_checker import DailyLimitChecker
from rate_limiter.tools.client_limit_fetcher import ClientLimitFetcher
from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants
from rate_limiter.tools.requests_per_second_counter import RequestsPerSecondCounter
from rate_limiter.tools.plans_collection_initializer import PlansCollectionInitializer
from rate_limiter.tools.clients_collection_initializer import (
    ClientsCollectionInitializer,
)


class RateLimiter:
    def __init__(self, mongo_client: MongoClient, redis_client: redis.Redis):
        # Initialize MongoDB and Redis connections
        self.mongo_client: MongoClient = mongo_client
        self.redis_client: redis.Redis = redis_client

        # Initialize MongoDB collections
        self.db: Database = self.mongo_client[RateLimiterConstants.SERVICE_MONGODB]
        self.plans_collection: Collection = self.db[
            RateLimiterConstants.PLANS_COLLECTION
        ]
        self.clients_collection: Collection = self.db[
            RateLimiterConstants.CLIENTS_COLLECTION
        ]

        # Tools
        self.plans_collection_initializer = PlansCollectionInitializer(
            plans_collection=self.plans_collection
        )
        self.clients_collection_initializer = ClientsCollectionInitializer(
            clients_collection=self.clients_collection
        )
        self.plans_fetcher = PlansFetcher(plans_collection=self.plans_collection)
        self.client_limit_fetcher = ClientLimitFetcher(
            redis_client=self.redis_client, clients_collection=self.clients_collection
        )
        self.requests_per_second_counter = RequestsPerSecondCounter(
            redis_client=self.redis_client
        )
        self.daily_limit_checker = DailyLimitChecker(redis_client=self.redis_client)

        # Local initializers for cache and collections
        self.clients_collection_initializer.run_tool()
        self.plans_collection_initializer.run_tool()
        self.plans_cache: Dict[str, Plan] = self.plans_fetcher.run_tool()

    def limit_exceeded(self, client_id: str) -> bool:
        daily_limit, second_limit = self.client_limit_fetcher.run_tool(
            client_id=client_id, plans_cache=self.plans_cache
        )

        count = self.requests_per_second_counter.run_tool(client_id=client_id)
        exceed_secondly_limit = count > second_limit

        if exceed_secondly_limit:
            print("Exceeding requests per second limit")
            # Maybe if request per second limit is exceeded we should sleep one second
            # in order not to lose the client's requests
            return True

        exceed_daily_limit = self.daily_limit_checker.run_tool(
            client_id=client_id,
            daily_limit=daily_limit,
        )

        if exceed_daily_limit:
            print("Exceeding requests per day limit")
            return True

        return False
