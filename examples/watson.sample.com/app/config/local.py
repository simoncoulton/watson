# -*- coding: utf-8 -*-
routes = {
    'home': {
        'path': '/',
        'defaults': {'controller': 'controllers.myrest.MyRest'}
    },
    'hello': {
        'path': '/hello',
        'defaults': {'controller': 'controllers.myaction.MyAction', 'action': 'hello'}
    },
    'world': {
        'path': '/world',
        'defaults': {'controller': 'controllers.myaction.MyAction', 'action': 'world'}
    },
    'json_world': {
        'path': '/hello-world.:format',
        'type': 'segment',
        'defaults': {
            'controller': 'controllers.myaction.MyAction',
            'action': 'json_world',
        },
        'requires': {'format': 'json$|xml$'}
    },
    'invalid_request': {
        'path': '/invalid',
        'defaults': {
            'controller': 'controllers.myaction.MyAction'
        }
    }
}
debug = {
    'profiling': {
        'enabled': False
    }
}
