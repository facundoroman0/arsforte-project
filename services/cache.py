import time
from functools import wraps
from django.core.cache import cache


def cached(ttl_seconds=900):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__module__}.{func.__name__}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        return wrapper
    return decorator
