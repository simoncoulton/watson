# -*- coding: utf-8 -*-
from watson.http.messages import create_request_from_environ
from watson.http.sessions import FileStorage, create_session_from_request
from tests.watson.http.support import sample_environ


class TestFunctions(object):
    def test_create_session_from_request(self):
        environ = sample_environ(HTTP_COOKIE='watson.session=12345')
        request = create_request_from_environ(environ)
        session = create_session_from_request(request)
        assert isinstance(session, FileStorage)
