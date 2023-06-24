from typing import TypedDict


class Plan(TypedDict):
    plan_id: str
    requests_per_second: int
    total_requests_per_day: int
