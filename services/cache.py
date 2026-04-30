import time
from functools import wraps
from django.core.cache import cache


def cached(ttl_seconds=900):
    """
    Decorador de cache para funciones sin argumentos o con argumentos hashable.
    Para funciones con argumentos complejos, usar cached_with_key().
    """
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


def cached_with_key(ttl_seconds=300):
    """
    Decorador de cache que genera claves basadas en argumentos.
    Args debe ser: (user, date, ...) donde el primer arg es user y el segundo es date.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = args[0] if args else kwargs.get('user')
            date_arg = args[1] if len(args) > 1 else kwargs.get('month_start') or kwargs.get('start_date')
            
            if user and date_arg:
                cache_key = f"{func.__module__}.{func.__name__}.{user.id}.{date_arg}"
            else:
                cache_key = f"{func.__module__}.{func.__name__}"
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        return wrapper
    return decorator
