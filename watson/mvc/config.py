# -*- coding: utf-8 -*-
# Default configuration for a Watson application.
# The container itself can be referenced by a simple lambda function such as:
# lambda container: container
#
# Consult the documentation for more indepth setting information.
import os
from watson.mvc import events

# Debug settings
debug = {
    'enabled': False,
    'panels': {
        'watson.debug.panels.request.Panel': {
            'enabled': True
        },
        'watson.debug.panels.application.Panel': {
            'enabled': True
        },
        'watson.debug.panels.profile.Panel': {
            'enabled': True,
            'max_results': 20,
            'sort': 'time',
        },
        'watson.debug.panels.framework.Panel': {
            'enabled': True
        },
    }
}

# IocContainer settings
dependencies = {
    'definitions': {
        'shared_event_dispatcher':
        {'item': 'watson.events.dispatcher.EventDispatcher'},
        'router': {
            'item': 'watson.mvc.routing.Router',
            'init':
            [lambda container: container.get(
             'application.config').get('routes',
                                       {})]
        },
        'profiler': {
            'item': 'watson.debug.profilers.Profiler',
            'init':
            [lambda container: container.get(
             'application.config')['debug']['profiling']]
        },
        'exception_handler': {
            'item': 'watson.mvc.exceptions.ExceptionHandler',
            'init':
            [lambda container: container.get(
             'application.config').get('debug',
                                       {})]
        },
        'jinja2_renderer': {
            'item': 'watson.renderers.Jinja2',
            'init': [
                lambda container: container.get('application.config')[
                    'views']['renderers']['default'].get('config', {}),
                lambda container: container.get('application')
            ]
        },
        'json_renderer': {'item': 'watson.renderers.Json'},
        'xml_renderer': {'item': 'watson.renderers.Xml'},
        'app_dispatch_execute_listener': {
            'item': 'watson.mvc.listeners.DispatchExecute',
            'init':
            [lambda container: container.get(
             'application.config')['views']['templates']]
        },
        'app_exception_listener': {
            'item': 'watson.mvc.listeners.Exception_',
            'init': [
                lambda container: container.get('exception_handler'),
                lambda container: container.get(
                    'application.config')['views']['templates']
            ]
        },
        'app_render_listener': {
            'item': 'watson.mvc.listeners.Render',
            'init':
            [lambda container: container.get(
             'application.config')['views']]
        }
    }
}

# View settings
views = {
    'default_format': 'html',
    'renderers': {
        'default': {
            'name': 'jinja2_renderer',
            'config': {
                'extension': 'html',
                'paths': [os.path.join(os.getcwd(), 'views')],
                'filters': ['watson.support.jinja2.filters'],
                'globals': ['watson.support.jinja2.globals']
            }
        },
        'xml': {'name': 'xml_renderer'},
        'json': {'name': 'json_renderer'}
    },
    'templates': {
        '404': 'errors/404',
        '500': 'errors/500'
    }
}

# Session settings
session = {
    'class': 'watson.http.sessions.File',
    'options': {
        'timeout': 3600
    }
}

# Application event settings
events = {
    events.EXCEPTION: [('app_exception_listener',)],
    events.INIT: [
        ('watson.debug.listeners.Init', 1, True)
    ],
    events.ROUTE_MATCH: [('watson.mvc.listeners.Route',)],
    events.DISPATCH_EXECUTE: [('app_dispatch_execute_listener',)],
    events.RENDER_VIEW: [('app_render_listener',)],
}
