# -*- coding: utf-8 -*-
# Runs an extremely simple web application on the development server
# that outputs some HTML. This is purely for demostration purposes, you
# should never return HTML directly from a controller.

import os
import sys

sys.path.append(os.path.abspath('..'))
from watson.mvc.applications import HttpApplication
from watson.mvc.controllers import RestController, ActionController
from watson.util.server import make_dev_server


class MyRestController(RestController):
    def GET(self):
        return '<h1>Welcome to Watson!</h1><a href="/hello">Hello</a> <a href="/world">World!</a>'


class MyActionController(ActionController):
    def hello_action(self):
        return '<a href="/world">Hello</a>'

    def world_action(self):
        return {'content': '<a href="/hello-world.json">World!</a>'}

    def json_world_action(self):
        return {'hello': 'world'}

application = HttpApplication({
    'routes': {
        'home': {
            'path': '/',
            'defaults': {'controller': 'simple_hello_world_wsgi_app.MyRestController'}
        },
        'hello': {
            'path': '/hello',
            'defaults': {'controller': 'simple_hello_world_wsgi_app.MyActionController', 'action': 'hello'}
        },
        'world': {
            'path': '/world',
            'defaults': {'controller': 'simple_hello_world_wsgi_app.MyActionController', 'action': 'world'}
        },
        'json_world': {
            'path': '/hello-world.:format',
            'type': 'segment',
            'defaults': {
                'controller': 'simple_hello_world_wsgi_app.MyActionController',
                'action': 'json_world',
            },
            'requires': {'format': 'json$'}
        },
        'invalid_request': {
            'path': '/invalid',
            'defaults': {
                'controller': 'simple_hello_world_wsgi_app.MyActionController'
            }
        }
    },
    'views': {
        'templates': {
            'myrestcontroller/get': 'blank',  # blank is a blank html template
            'myactioncontroller/hello': 'blank',  # the first module is stripped from the path
            'myactioncontroller/world': 'blank',
        }
    }
})

if __name__ == '__main__':
    make_dev_server(application, do_reload=True)
