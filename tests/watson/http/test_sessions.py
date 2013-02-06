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
    def test_create(self):
        session = FileStorage(id=123, timeout=30, autosave=False)
        session['test'] = 'blah'
        assert session.timeout == 30
        assert session.autosave == False
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
        assert session.data == None

    def test_load(self):
        session = FileStorage()
        session.load()

    def test_load_existing_data(self):
        session = FileStorage(timeout=-1)
        session['blah'] = 'test'
        session.load()
        assert session['blah'] == None

    def test_exists(self):
        session = FileStorage()
        assert not session.exists()


class TestMemoryStorage(object):
    def test_create(self):
        session = MemoryStorage(id=123, timeout=30, autosave=False)
        session['test'] = 'blah'
        assert session.timeout == 30
        assert session.autosave == False
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
        assert session.data == None

    def test_load(self):
        session = MemoryStorage()
        session.load()

    def test_load_existing_data(self):
        session = MemoryStorage(timeout=-1)
        session['blah'] = 'test'
        session.load()
        assert session['blah'] == None

    def test_exists(self):
        session = MemoryStorage()
        assert not session.exists()


class TestFunctions(object):
    def test_create_session_from_request(self):
        environ = {}
        util.setup_testing_defaults(environ)
        environ['HTTP_COOKIE'] = 'watson.session=12345'
        request = create_request_from_environ(environ)
        session = create_session_from_request(request)
        assert isinstance(session, FileStorage)
