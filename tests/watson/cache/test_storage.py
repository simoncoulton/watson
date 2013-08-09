# -*- coding: utf-8 -*-
from unittest.mock import Mock
from tempfile import gettempdir
from nose.tools import raises
from watson.cache.storage import BaseStorage, Memory, File, Memcached


class TestBaseStorage(object):

    def test_create(self):
        bs = BaseStorage()
        assert repr(bs) == '<watson.cache.storage.BaseStorage>'

    @raises(NotImplementedError)
    def test_set(self):
        bs = BaseStorage()
        bs['test'] = 'test'

    @raises(NotImplementedError)
    def test_set_params(self):
        bs = BaseStorage()
        bs.set('test', 'test', timeout=3600)

    @raises(NotImplementedError)
    def test_get(self):
        bs = BaseStorage()
        bs['test']

    @raises(NotImplementedError)
    def test_get_default(self):
        bs = BaseStorage()
        bs.get('test')

    @raises(NotImplementedError)
    def test_delete(self):
        bs = BaseStorage()
        del bs['test']

    @raises(NotImplementedError)
    def test_contains(self):
        bs = BaseStorage()
        'test' in bs

    @raises(NotImplementedError)
    def test_flush(self):
        bs = BaseStorage()
        bs.flush()

    @raises(NotImplementedError)
    def test_expired(self):
        bs = BaseStorage()
        bs.expired('some_key')


class TestMemory(object):

    def test_create(self):
        cache = Memory()
        assert repr(cache) == '<watson.cache.storage.Memory>'

    def test_set(self):
        cache = Memory()
        cache['test'] = 'test'
        cache.set('expired', 'value', -1)
        assert cache['test'] == 'test'
        assert not cache['expired']

    def test_get(self):
        cache = Memory()
        cache['test'] = 'test'
        assert cache['test'] == 'test'
        assert cache.get('test') == 'test'
        assert cache.get('invalid', 'blah') == 'blah'

    def test_delete(self):
        cache = Memory()
        cache['test'] = 'test'
        assert cache['test'] == 'test'
        del cache['test']
        assert not cache['test']

    def test_flush(self):
        cache = Memory()
        cache['test'] = 'test'
        assert cache.flush()
        assert not cache['test']

    def test_expired(self):
        cache = Memory()
        cache.set('test', 'value', -1)
        assert cache.expired('test')

    def test_contains(self):
        cache = Memory()
        assert not 'test' in cache
        cache['test'] = 'test'
        assert 'test' in cache


class TestMemcache(object):

    def setup(self):
        self.mock_memcache = Mock()

    def test_create(self):
        cache = Memcached()
        assert repr(cache) == '<watson.cache.storage.Memcached servers:1>'

    def test_create_custom_config(self):
        cache = Memcached({
            'servers': ['127.0.0.1:11211', '192.168.100.1:11211']
        })
        assert repr(cache) == '<watson.cache.storage.Memcached servers:2>'

    @raises(ImportError)
    def test_open(self):
        cache = Memcached()
        cache.open()

    def test_set(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.client.get.return_value = 'test'
        cache.flush()
        cache['test'] = 'test'
        assert cache['test'] == 'test'

    def test_set_expired(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.client.get.return_value = None
        cache.flush()
        cache.set('expired', 'value', -1)
        assert not cache['expired']

    def test_get(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.flush()
        cache['test'] = 'test'
        cache.client.get.return_value = 'test'
        assert cache['test'] == 'test'
        assert cache.get('test') == 'test'
        cache.client.get.return_value = 'blah'
        assert cache.get('invalid', 'blah') == 'blah'

    def test_delete(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.flush()
        cache.client.get.return_value = 'test'
        cache['test'] = 'test'
        assert cache['test'] == 'test'
        del cache['test']
        cache.client.get.return_value = None
        assert not cache['test']

    def test_flush(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.flush()
        cache.client.get.return_value = None
        cache['test'] = 'test'
        assert cache.flush()
        assert not cache['test']

    def test_expired(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.flush()
        cache.set('test', 'value', -1)
        cache.client.get.return_value = None
        assert cache.expired('test')

    def test_contains(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        cache.client.get.return_value = False
        cache.flush()
        assert not 'test' in cache
        cache['test'] = 'test'
        cache.client.get.return_value = True
        assert 'test' in cache

    def test_close(self):
        cache = Memcached()
        cache.client = self.mock_memcache
        assert cache.close()


class TestFile(object):

    def test_create(self):
        cache = File()
        assert repr(cache) == '<watson.cache.storage.File dir:{0}>'.format(
            gettempdir())

    def test_create_custom_config(self):
        cache = File({'dir': '/tmp'})
        assert repr(cache) == '<watson.cache.storage.File dir:/tmp>'

    def test_set(self):
        cache = File()
        cache.flush()
        cache['test'] = 'test'
        cache.set('expired', 'value', -1)
        assert cache['test'] == 'test'
        assert not cache['expired']

    def test_delete(self):
        cache = File()
        cache.flush()
        cache['test'] = 'test'
        assert cache['test'] == 'test'
        del cache['test']
        assert not cache['test']

    def test_delete_invalid(self):
        cache = File()
        cache.flush()
        del cache['test']

    def test_get(self):
        cache = File()
        cache.flush()
        cache['test'] = 'test'
        assert cache['test'] == 'test'
        assert cache.get('test') == 'test'
        assert cache.get('invalid', 'blah') == 'blah'

    def test_get_invalid(self):
        cache = File()
        cache.flush()

    def test_expired(self):
        cache = File()
        cache.flush()
        cache.set('test', 'value', -1)
        assert cache.expired('test')

    def test_contains(self):
        cache = File()
        cache.flush()
        assert not 'test' in cache
        cache['test'] = 'test'
        assert 'test' in cache

    def test_flush(self):
        cache = File()
        cache.flush()
        cache['test'] = 'test'
        assert cache.flush()
        assert not cache['test']
