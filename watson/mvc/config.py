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
    'profiling': {
        'enabled': False,
        'max_results': 20,
        'sort': 'cumulative',
    }
}

# IocContainer settings
dependencies = {
    'definitions': {
        'shared_event_dispatcher': {'item': 'watson.events.dispatcher.EventDispatcher'},
        'router': {
            'item': 'watson.mvc.routing.Router',
            'init': [lambda container: container.get('application.config').get('routes', {})]
        },
        'profiler': {
            'item': 'watson.debug.profilers.Profiler',
            'init': [lambda container: container.get('application.config')['debug']['profiling']]
        },
        'exception_handler': {
            'item': 'watson.mvc.exceptions.ExceptionHandler',
            'init': [lambda container: container.get('application.config').get('debug', {})]
        },
        'jinja2_renderer': {
            'item': 'watson.mvc.views.Jinja2Renderer',
            'init': [lambda container: container.get('application.config')['views']['renderers']['default'].get('config', {})]
        },
        'json_renderer': {'item': 'watson.mvc.views.JsonRenderer'},
        'xml_renderer': {'item': 'watson.mvc.views.XmlRenderer'},
        'app_dispatch_execute_listener': {
            'item': 'watson.mvc.listeners.DispatchExecuteListener',
            'init': [lambda container: container.get('application.config')['views']['templates']]
        },
        'app_exception_listener': {
            'item': 'watson.mvc.listeners.ExceptionListener',
            'init': [
                lambda container: container.get('exception_handler'),
                lambda container: container.get('application.config')['views']['templates']
            ]
        },
        'app_render_listener': {
            'item': 'watson.mvc.listeners.RenderListener',
            'init': [lambda container: container.get('application.config')['views']]
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
                'paths': [os.path.join(os.getcwd(), 'views')]
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
    'class': 'watson.http.sessions.FileStorage'
}

# Application event settings
events = {
    events.EXCEPTION_EVENT: [('app_exception_listener',)],
    events.INIT_EVENT: [
        ('watson.debug.profilers.ApplicationInitListener', 1, True)
    ],
    events.ROUTE_MATCH_EVENT: [('watson.mvc.listeners.RouteListener',)],
    events.DISPATCH_EXECUTE_EVENT: [('app_dispatch_execute_listener',)],
    events.RENDER_VIEW_EVENT: [('app_render_listener',)],
}
