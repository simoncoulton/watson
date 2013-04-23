# -*- coding: utf-8 -*-
from watson.http.messages import create_request_from_environ
from watson.http.sessions import FileStorage, SessionMixin
from tests.watson.http.support import sample_environ


class TestSessionMixin(object):
    def test_session_from_request(self):
        environ = sample_environ(HTTP_COOKIE='watson.session=12345')
        request = create_request_from_environ(environ)
        assert isinstance(request.session, FileStorage)
        assert isinstance(request, SessionMixin)
