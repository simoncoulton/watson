# -*- coding: utf-8 -*-
import os
from watson.mvc import events

debug = {
    'profiling': {
        'enabled': False,
        'max_results': 20,
        'sort': 'cumulative',
    }
}
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
        'dispatch_execute_listener': {
            'item': 'watson.mvc.listeners.DispatchExecuteListener',
            'init': [lambda container: container.get('application.config')['views']['templates']]
        }
    }
}
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
events = {
    events.EXCEPTION_EVENT: [('watson.mvc.listeners.ExceptionListener',)],
    events.INIT_EVENT: [
        ('watson.debug.profilers.ApplicationInitListener', 1, True)
    ],
    events.ROUTE_MATCH_EVENT: [('watson.mvc.listeners.RouteListener',)],
    events.DISPATCH_EXECUTE_EVENT: [('dispatch_execute_listener',)],
    events.RENDER_VIEW_EVENT: [('watson.mvc.listeners.RenderListener',)],
}
