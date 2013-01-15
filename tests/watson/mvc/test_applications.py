# -*- coding: utf-8 -*-
from wsgiref import util
from watson.di.container import IocContainer
from watson.mvc.applications import WsgiApplication, DEFAULTS


def start_response(status_line, headers):
    pass


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


class TestWsgiApplication(object):
    def test_create(self):
        application = WsgiApplication()
        assert isinstance(application.container, IocContainer)
        assert application.config == DEFAULTS

    def test_call(self):
        application = WsgiApplication()
        response = application(sample_environ(), start_response)
        print(response)


class TestConsoleApplication(object):
    pass
