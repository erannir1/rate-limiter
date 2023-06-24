# import unittest
# from unittest.mock import MagicMock
#
# from rate_limiter.tools.requests_per_second_counter import RequestsPerSecondCounter
#
#
# class RequestsPerSecondCounterTests(unittest.TestCase):
#     @classmethod
#     def setUp(cls):
#         cls.redis_client = MagicMock()
#         cls.counter = RequestsPerSecondCounter(cls.redis_client)
#
#     @classmethod
#     def tearDownClass(cls):
#         # Clean up the Redis client
#         cls.redis_client.close()
#
#     def test_increment_counter(self):
#         key = "client1:123456"
#         self.redis_client.incr.return_value = 5
#         count = self.counter.increment_counter(key)
#         self.assertEqual(count, 5)
#         self.redis_client.incr.assert_called_once_with(key)
#
#     def test_expire_counter(self):
#         key = "client1:123456"
#         self.counter.expire_counter(key)
#         self.redis_client.expire.assert_called_once_with(key, 60)
#
#     def test_run_tool(self):
#         client_id = "client1"
#         current_time = 1234567890
#         key = f"{client_id}:{current_time}"
#         self.counter.increment_counter = MagicMock(return_value=10)
#         self.counter.expire_counter = MagicMock()
#
#         with unittest.mock.patch('time.time', return_value=current_time):
#             count = self.counter.run_tool(client_id)
#
#         self.assertEqual(count, 10)
#         self.counter.increment_counter.assert_called_once_with(key)
#         self.counter.expire_counter.assert_called_once_with(key)
#
#
# if __name__ == '__main__':
#     unittest.main()


import unittest
from unittest.mock import MagicMock, patch
import datetime

from rate_limiter.tools.requests_per_second_counter import RequestsPerSecondCounter


class RequestsPerSecondCounterTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.redis_client = MagicMock()
        cls.counter = RequestsPerSecondCounter(cls.redis_client)

    @classmethod
    def tearDownClass(cls):
        # Clean up the Redis client
        cls.redis_client.close()

    def test_increment_counter(self):
        key = "client1:123456"
        self.redis_client.incr.return_value = 5
        count = self.counter.increment_counter(key)
        self.assertEqual(count, 5)
        self.redis_client.incr.assert_called_once_with(key)

    def test_expire_counter(self):
        key = "client1:123456"
        self.counter.expire_counter(key)
        self.redis_client.expire.assert_called_once_with(key, 60)

    @patch("datetime.datetime")
    def test_run_tool(self, mock_datetime):
        client_id = "client1"
        current_datetime = datetime.datetime(2023, 6, 24, 12, 0, 0)
        current_time = 1234567890
        key = f"{client_id}:{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}"

        self.counter.increment_counter = MagicMock(return_value=10)
        self.counter.expire_counter = MagicMock()

        mock_datetime.utcnow.return_value = current_datetime
        with patch("time.time", return_value=current_time):
            count = self.counter.run_tool(client_id)

        self.assertEqual(count, 10)
        self.counter.increment_counter.assert_called_once_with(key)
        self.counter.expire_counter.assert_called_once_with(key)


if __name__ == "__main__":
    unittest.main()
