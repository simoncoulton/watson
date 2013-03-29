# -*- coding: utf-8 -*-
from watson.di.container import IocContainer
from watson.mvc.applications import HttpApplication
from watson.mvc import config
from watson.mvc.controllers import RestController
from watson.common.datastructures import module_to_dict
from tests.watson.mvc.support import sample_environ, start_response


class TestHttpApplication(object):
    def test_create(self):
        application = HttpApplication()
        assert isinstance(application.container, IocContainer)
        assert application.config == module_to_dict(config, '__')

    def test_call(self):
        application = HttpApplication({
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
