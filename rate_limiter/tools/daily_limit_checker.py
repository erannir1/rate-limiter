import datetime


class DailyLimitChecker:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def run_tool(self, client_id: str, daily_limit: int) -> bool:
        today: str = datetime.date.today().strftime("%Y-%m-%d")
        daily_count_key: str = f"{client_id}:daily_count:{today}"
        daily_count = self.redis_client.get(daily_count_key)

        if daily_count is None:
            daily_count = 0
        else:
            daily_count = int(daily_count.decode())

        daily_count += 1
        self.redis_client.set(daily_count_key, daily_count)
        exceeded_daily_limit = daily_count > daily_limit
        print(f"daily count: {daily_count}")
        return exceeded_daily_limit
