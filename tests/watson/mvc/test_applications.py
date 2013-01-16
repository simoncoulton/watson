# -*- coding: utf-8 -*-
from wsgiref import util
from watson.di.container import IocContainer
from watson.mvc.applications import WsgiApplication, DEFAULTS
from watson.mvc.controllers import RestController


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
        application = WsgiApplication({
            'routes': {
                'home': {
                    'path': '/',
                    'defaults': {
                        'controller': 'tests.watson.mvc.test_applications.TestController'
                    }
                }
            },
            'views': {
                'templates': {
                    'watson/mvc/test_applications/testcontroller/post': 'blank'
                }
            }
        })
        response = application(sample_environ(PATH_INFO='/', REQUEST_METHOD='POST', HTTP_ACCEPT='application/json'), start_response)
        assert response == [b'{"content": "Posted Hello World!"}']


class TestConsoleApplication(object):
    pass


class TestController(RestController):
    def GET(self):
        return 'Hello World!'

    def POST(self):
        return 'Posted Hello World!'
