# -*- coding: utf-8 -*-
from watson.cache.storage import BaseStorage, Memory, File, Memcached
from watson.cache.decorators import cache
from watson.di.container import IocContainer


class TestCacheDecorator(object):
    def test_get(self):
        c = SampleClass()
        print(c.run())
        print(c.run())


class SampleClass(object):
    def __init__(self):
        self.container = IocContainer({
            'definitions': {
                'cache': {'item': 'watson.cache.storage.Memory'}
            }
        })

    @cache(timeout=60, key='some_key')
    def run(self):
        return 'a'
