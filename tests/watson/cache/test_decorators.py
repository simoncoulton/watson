# -*- coding: utf-8 -*-
from tests.watson.cache.support import AClass, SampleClass


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
        assert not memcached_instance[
            'tests.watson.cache.support.SampleClass.tada']
        assert c.tada() == 'test'
        assert memcached_instance[
            'tests.watson.cache.support.SampleClass.tada'] == 'test'

    def test_get_no_container(self):
        a = AClass()
        assert a.run() == 'test'
