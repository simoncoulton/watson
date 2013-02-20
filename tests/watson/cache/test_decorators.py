# -*- coding: utf-8 -*-
from watson.cache.decorators import cache
from watson.di.container import IocContainer


class TestCacheDecorator(object):
    def test_get_key(self):
        c = SampleClass()
        memcached_instance = c.container.get('watson.cache.storage.Memory')
        assert not memcached_instance['some_key']
        assert c.run() == 'test'
        assert memcached_instance['some_key'] == 'test'

    def test_get_no_key(self):
        c = SampleClass()
        memcached_instance = c.container.get('watson.cache.storage.Memory')
        assert not memcached_instance['tests.watson.cache.test_decorators.SampleClass.tada']
        assert c.tada() == 'test'
        assert memcached_instance['tests.watson.cache.test_decorators.SampleClass.tada'] == 'test'

    def test_get_no_container(self):
        a = AClass()
        assert a.run() == 'test'


class AClass(object):
    @cache
    def run(self):
        return 'test'


class SampleClass(object):
    def __init__(self):
        self.container = IocContainer({
            'definitions': {
                'application.config': {'item': {'cache': {'type': 'watson.cache.storage.Memory'}}}
            }
        })

    @cache(timeout=60, key='some_key')
    def run(self):
        return 'test'

    @cache
    def tada(self):
        return 'test'
