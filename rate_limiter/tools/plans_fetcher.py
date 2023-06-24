from typing import Dict

from pymongo.collection import Collection

from rate_limiter.types.plan import Plan
from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants


class PlansFetcher:
    def __init__(self, plans_collection: Collection):
        self.plans_collection: Collection = plans_collection

    def run_tool(self) -> Dict[str, Plan]:
        plans_cache = {}
        # Retrieve all plans from MongoDB and populate the plan cache
        plans = self.plans_collection.find({}, {"_id": 0})
        for plan in plans:
            plans_cache[plan[RateLimiterConstants.PLAN_ID]]: Plan = plan
        return plans_cache
