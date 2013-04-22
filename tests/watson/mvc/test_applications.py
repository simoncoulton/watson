# -*- coding: utf-8 -*-
from watson.di.container import IocContainer
from watson.mvc.applications import HttpApplication, ConsoleApplication
from watson.mvc import config
from watson.common.datastructures import module_to_dict
from tests.watson.mvc.support import sample_environ, start_response, SampleNonStringCommand
from tests.watson.mvc import sample_config


class TestHttpApplication(object):
    def test_create(self):
        application = HttpApplication()
        assert isinstance(application.container, IocContainer)
        assert application.config == module_to_dict(config, '__')
        application_module = HttpApplication(sample_config)
        assert application_module.config['debug']['enabled']

    def test_call(self):
        application = HttpApplication({
            'routes': {
                'home': {
                    'path': '/',
                    'defaults': {
                        'controller': 'tests.watson.mvc.support.TestController'
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
    def test_create(self):
        application = ConsoleApplication()
        assert isinstance(application.container, IocContainer)

    def test_register_commands(self):
        application = ConsoleApplication({
            'commands': ['tests.watson.mvc.support.SampleStringCommand',
                         SampleNonStringCommand]
        })
        assert len(application.config['commands']) == 2

    def test_execute_command(self):
        application = ConsoleApplication({
            'commands': ['tests.watson.mvc.support.SampleStringCommand',
                         SampleNonStringCommand]
        }, ['py.test', 'string'])
        assert application() == 'Executed!'
