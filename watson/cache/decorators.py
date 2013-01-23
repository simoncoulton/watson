# -*- coding: utf-8 -*-
from functools import wraps


def cache(timeout=0, key=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_instance = self.container.get('cache')  # todo: pull this from config
            key_name = key if key else func.__name__
            if key_name not in cache_instance:
                cache_instance.set(key_name, func(self, *args, **kwargs), timeout)
            return cache_instance[key_name]
        return wrapper
    return decorator
