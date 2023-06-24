from typing import List

from pymongo.collection import Collection

from rate_limiter.types.plan import Plan
from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants


class PlansCollectionInitializer:
    def __init__(self, plans_collection: Collection):
        self.plans_collection: Collection = plans_collection

    def run_tool(self):
        if self.plans_collection.count_documents({}) == 0:
            default_plans: List[Plan] = [
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
            self.plans_collection.insert_many(default_plans)
