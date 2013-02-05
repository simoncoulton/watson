# -*- coding: utf-8 -*-
from functools import wraps
from watson.stdlib.imports import get_qualified_name


def cache(timeout=0, key=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_config = self.container.get('application.config')['cache']
            cache_instance = self.container.get(cache_config['type'])
            key_name = key if key else get_qualified_name(func)
            if key_name not in cache_instance:
                cache_instance.set(key_name, func(self, *args, **kwargs), timeout)
            return cache_instance[key_name]
        return wrapper
    return decorator
