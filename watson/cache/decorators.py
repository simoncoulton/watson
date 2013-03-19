# -*- coding: utf-8 -*-
from watson.cache.storage import Memory
from watson.stdlib.imports import get_qualified_name

DEFAULT_CACHE_TYPE = Memory


def cache(func=None, timeout=0, key=None):
    """Retrieve a value from the cache

    Attempts to retrieve a value from the cache. If the wrapped function
    does not have an attribute of container (see watson.di.container), from
    which to retrieve the cache type then it will default to cache.storage.Memory.

    Args:
        callable func: the function that is being wrapped
        int timeout: the number of seconds the item should exist in the cache
        string key: the key to store the data against in the cache, defaults
            to the qualified name of the decorated function.

    Returns:
        The contents of the cache key.

    Usage:
        class MyClass(ContainerAware):
            @cache(timeout=3600)
            def expensive_func(self):
                return 'something'

        c = MyClass()
        c.expensive_func() # something
        c.expensive_func() # something - returned from cache
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'container'):
                cache_instance = DEFAULT_CACHE_TYPE()
            else:
                cache_config = self.container.get('application.config')['cache']
                cache_instance = self.container.get(cache_config['type'])
            key_name = key if key else get_qualified_name(func)
            if key_name not in cache_instance:
                cache_instance.set(key_name, func(self, *args, **kwargs), timeout)
            return cache_instance[key_name]
        return wrapper
    if func:
        return decorator(func)
    else:
        return decorator
