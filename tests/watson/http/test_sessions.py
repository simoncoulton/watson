# -*- coding: utf-8 -*-
from wsgiref import util
from nose.tools import raises
from watson.http.messages import create_request_from_environ
from watson.http.sessions import StorageMixin, FileStorage, MemoryStorage, create_session_from_request


class TestStorageMixin(object):
    def test_create(self):
        session = StorageMixin(id=123, timeout=30, autosave=False)
        session['test'] = 'blah'
        assert session.timeout == 30
        assert session.autosave == False
        assert session.id == 123
        assert repr(session) == '<watson.http.sessions.StorageMixin id:123>'
        assert session['test'] == 'blah'
        assert session.get('test') == 'blah'

    def test_cookie_params(self):
        session = StorageMixin()
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
        session = StorageMixin()
        assert session.data == None

    @raises(Exception)
    def test_missing_load_implementation(self):
        session = StorageMixin()
        session._load()

    @raises(Exception)
    def test_missing_save_implementation(self):
        session = StorageMixin()
        session._save()

    @raises(Exception)
    def test_missing_destroy_implementation(self):
        session = StorageMixin()
        session._destroy()

    @raises(Exception)
    def test_missing_exists_implementation(self):
        session = StorageMixin()
        session._exists()


class TestFileStorage(object):
    pass


class TestMemoryStorage(object):
    pass


class TestFunctions(object):
    def test_create_session_from_request(self):
        environ = {}
        util.setup_testing_defaults(environ)
        environ['HTTP_COOKIE'] = 'watson.session=12345'
        request = create_request_from_environ(environ)
        session = create_session_from_request(request)
        assert isinstance(session, FileStorage)
