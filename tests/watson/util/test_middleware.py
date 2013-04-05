# -*- coding: utf-8 -*-
import os
from watson.util.middleware import StaticFileMiddleware
from tests.watson.util.support import sample_app, sample_environ, sample_start_response


class TestStaticFileMiddleware(object):
    def setup(self):
        self.old_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def teardown(self):
        os.chdir(self.old_path)

    def test_create(self):
        mw = StaticFileMiddleware(sample_app)
        assert mw.app == sample_app
        assert mw.initial_dir == os.getcwd()

    def test_execute(self):
        mw = StaticFileMiddleware(sample_app)
        environ = sample_environ(PATH_INFO='/sample.css')
        response = mw(environ, sample_start_response)
        assert response == [b'html, body { background: red; }']

    def test_execute_serve_directory(self):
        mw = StaticFileMiddleware(sample_app)
        environ = sample_environ(PATH_INFO='/')
        response = mw(environ, sample_start_response)
        assert response
