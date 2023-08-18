import time
import typing
from threading import Lock
from datetime import datetime, timedelta
from typing import Dict

from ratelimit import RateLimitDecorator
from ratelimiter import RateLimiter


class KeyManager:
    def __init__(self, api_key_list, sleep_time=2, seconds=3, max_calls=60):
        self.lock = Lock()
        self.seconds = seconds
        self.sleep_time = sleep_time
        self.max_calls = max_calls
        self.rate_limiters: Dict[str: RateLimiter] = {}

        for key in api_key_list:
            self.rate_limiters[key] = RateLimitDecorator(
                calls=max_calls,
                period=seconds,
                raise_on_limit=False,
            )(lambda x: x)

    def assign(self):
        with self.lock:
            while 1:
                for key, rate_limiter in self.rate_limiters.items():
                    if key := rate_limiter(key):
                        return key
                time.sleep(self.sleep_time)


def inject_param_decorator(**inject_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 在调用函数之前，注入额外参数
            for kwargs_key, kwargs_value in inject_kwargs.items():
                if isinstance(kwargs_value, typing.Callable):
                    kwargs_value = kwargs_value()
                kwargs[kwargs_key] = kwargs_value
            return func(*args, **kwargs)
        return wrapper
    return decorator