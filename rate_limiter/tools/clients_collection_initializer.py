from typing import List

from pymongo.collection import Collection

from auth import accounts
from rate_limiter.types.client_doc import ClientDoc
from rate_limiter.tools.rate_limiter_constants import RateLimiterConstants


class ClientsCollectionInitializer:
    def __init__(self, clients_collection: Collection):
        self.clients_collection: Collection = clients_collection

    def run_tool(self):
        if self.clients_collection.count_documents({}) == 0:
            default_clients_plans: List[ClientDoc] = [
                {
                    RateLimiterConstants.CLIENT_ID: k,
                    RateLimiterConstants.PLAN: v[RateLimiterConstants.PLAN],
                }
                for k, v in accounts.items()
            ]

            self.clients_collection.insert_many(default_clients_plans)
