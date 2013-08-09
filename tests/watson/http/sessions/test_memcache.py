# -*- coding: utf-8 -*-
import datetime
from unittest.mock import Mock
from nose.tools import raises
from watson.http import sessions


class TestMemcacheStorage(object):

    def setup(self):
        self.mock_memcache = Mock()

    def test_create(self):
        session = sessions.Memcache(id=123, timeout=30, autosave=False)
        assert session.autosave is False
        assert session.timeout == 30
        assert session.id == 123

    @raises(ImportError)
    def test_open_connection(self):
        session = sessions.Memcache()
        session.open()

    def test_cookie_params(self):
        session = sessions.Memcache()
        params = {
            'expires': 0,
            'path': '/',
            'domain': None,
            'secure': False,
            'httponly': True,
            'comment': 'Watson session id'
        }
        session.cookie_params = params
        assert session.cookie_params == params

    def test_data(self):
        session = sessions.Memcache()
        assert session.data is None

    def test_load(self):
        session = sessions.Memcache()
        session.client = self.mock_memcache
        session.client.get.return_value = {}
        session.load()
        assert not session.data

    def test_load_existing_data(self):
        session = sessions.Memcache(timeout=-1)
        session.client = self.mock_memcache
        session.client.get.return_value = None
        session['blah'] = 'test'
        session.load()
        assert session['blah'] is None

    def test_exists(self):
        session = sessions.Memcache()
        session.client = self.mock_memcache
        session.client.get.return_value = None
        assert not session.exists()

    def test_close(self):
        session = sessions.Memcache()
        session.client = self.mock_memcache
        assert session.close()

    def test_destroy(self):
        session = sessions.Memcache()
        session.client = self.mock_memcache
        session['test'] = 'blah'
        session.client.get.return_value = 'blah'
        assert session['test'] == 'blah'
        session.destroy()
        assert not session.exists()
