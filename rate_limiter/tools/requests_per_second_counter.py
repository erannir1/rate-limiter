import datetime


class RequestsPerSecondCounter:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def run_tool(self, client_id: str) -> int:
        # The use of datetime.datetime.utcnow() is for the very extreme edge case
        # of multiple servers located in different timezones
        current_datetime = datetime.datetime.utcnow()
        key: str = f"{client_id}:{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        count: int = self.increment_counter(key)
        self.expire_counter(key)
        return count

    def increment_counter(self, key: str) -> int:
        count: int = self.redis_client.incr(key)
        return count

    def expire_counter(self, key: str):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        self.redis_client.expireat(key, expiration_time)
