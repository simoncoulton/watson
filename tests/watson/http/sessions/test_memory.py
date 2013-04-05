# -*- coding: utf-8 -*-
from watson.http.sessions import MemoryStorage


class TestMemoryStorage(object):
    def test_create(self):
        session = MemoryStorage(id=123, timeout=30, autosave=False)
        session['test'] = 'blah'
        assert session.timeout == 30
        assert session.autosave is False
        assert session.id == 123
        assert repr(session) == '<watson.http.sessions.MemoryStorage id:123>'
        assert session['test'] == 'blah'
        assert session.get('test') == 'blah'

    def test_cookie_params(self):
        session = MemoryStorage()
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
        session = MemoryStorage()
        assert session.data is None

    def test_load(self):
        session = MemoryStorage()
        session.load()

    def test_load_existing_data(self):
        session = MemoryStorage(timeout=-1)
        session['blah'] = 'test'
        session.load()
        assert session['blah'] is None

    def test_exists(self):
        session = MemoryStorage()
        assert not session.exists()

    def test_delete_key(self):
        # testing here as _load is not implemented in StorageMixin
        session = MemoryStorage()
        session._data = {'test': 'value'}
        del session['test']
        del session['invalid_key']
        assert 'test' not in session

    def test_iterate_data(self):
        # testing here as _load is not implemented in StorageMixin
        session = MemoryStorage()
        session['test'] = 'value'
        for key, value in session:
            assert(True)
            break
        else:
            assert(False)
