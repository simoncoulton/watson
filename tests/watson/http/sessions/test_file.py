# -*- coding: utf-8 -*-
from watson.http.sessions import FileStorage


class TestFileStorage(object):
    def test_create(self):
        session = FileStorage(id=123, timeout=30, autosave=False)
        session['test'] = 'blah'
        assert session.timeout == 30
        assert session.autosave is False
        assert session.id == 123
        assert repr(session) == '<watson.http.sessions.FileStorage id:123>'
        assert session['test'] == 'blah'
        assert session.get('test') == 'blah'

    def test_custom_storage_path(self):
        session = FileStorage(storage='/tmp')
        assert session.storage == '/tmp'

    def test_cookie_params(self):
        session = FileStorage()
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
        session = FileStorage()
        assert session.data is None

    def test_load(self):
        session = FileStorage()
        session.load()

    def test_load_existing_data(self):
        session = FileStorage(timeout=-1)
        session['blah'] = 'test'
        session.load()
        assert session['blah'] is None

    def test_exists(self):
        session = FileStorage()
        assert not session.exists()
