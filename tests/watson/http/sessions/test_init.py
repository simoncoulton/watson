# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.http.messages import create_request_from_environ
from watson.http import sessions
from tests.watson.http.support import sample_environ


class TestSessionMixin(object):

    def test_session_from_request(self):
        environ = sample_environ(HTTP_COOKIE='watson.session=12345')
        request = create_request_from_environ(environ)
        assert isinstance(request.session, sessions.File)
        assert isinstance(request, sessions.SessionMixin)

    def test_session_from_https_request(self):
        environ = sample_environ(HTTPS='HTTPS')
        request = create_request_from_environ(environ)
        assert request.is_secure()
        request.session_to_cookie()
        cookie = request.cookies[sessions.COOKIE_KEY]
        assert cookie['httponly']
        assert cookie['secure']

    @raises(Exception)
    def test_session_cant_save(self):
        mixin = sessions.StorageMixin()
        mixin.save()

    @raises(NotImplementedError)
    def test_session_load_iter(self):
        mixin = sessions.StorageMixin()
        for key, value in mixin:
            assert True
