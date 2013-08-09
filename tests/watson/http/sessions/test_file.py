# -*- coding: utf-8 -*-
from watson.http import sessions


class TestFile(object):

    def test_create(self):
        session = sessions.File(id=123, timeout=30, autosave=False)
        session['test'] = 'blah'
        assert session.timeout == 30
        assert session.autosave is False
        assert session.id == 123
        assert repr(session) == '<watson.http.sessions.file.Storage id:123>'
        assert session['test'] == 'blah'
        assert session.get('test') == 'blah'

    def test_custom_storage_path(self):
        session = sessions.File(storage='/tmp')
        assert session.storage == '/tmp'

    def test_cookie_params(self):
        session = sessions.File()
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
        session = sessions.File()
        assert session.data is None

    def test_load(self):
        session = sessions.File()
        session.load()

    def test_load_existing_data(self):
        session = sessions.File(timeout=-1)
        session['blah'] = 'test'
        session.load()
        assert session['blah'] is None

    def test_exists(self):
        session = sessions.File()
        assert not session.exists()
