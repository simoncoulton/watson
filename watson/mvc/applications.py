# -*- coding: utf-8 -*-
import os
from watson.di import ContainerAware
from watson.di.container import IocContainer
from watson.events.dispatcher import EventDispatcherAware
from watson.events.types import Event
from watson.http.messages import create_request_from_environ, Response
from watson.mvc.exceptions import ApplicationError
from watson.stdlib.datastructures import dict_deep_update


ROUTE_MATCH_EVENT = 'event.application.route.match'
DISPATCH_EXECUTE_EVENT = 'event.application.dispatch.execute'
RENDER_EVENT = 'event.application.render'
EXCEPTION_EVENT = 'event.application.exception'
DEFAULTS = {
    'routes': {},
    'dependencies': {
        'definitions': {
            'shared_event_dispatcher': {
                'item': 'watson.events.dispatcher.EventDispatcher'
            },
            'router': {
                'item': 'watson.mvc.routing.Router',
                'init': [lambda container: container.get('application.config').get('routes', {})]
            },
            'route_listener': {'item': 'watson.mvc.listeners.RouteListener'},
            'controller_dispatch_listener': {'item': 'watson.mvc.listeners.DispatchListener'},
            'exception_listener': {'item': 'watson.mvc.listeners.ExceptionListener'},
            'render_listener': {'item': 'watson.mvc.listeners.RenderListener'},
            'jinja2_renderer': {
                'item': 'watson.mvc.views.Jinja2Renderer',
                'init': [lambda container: container.get('application.config')['views']['renderers']['default'].get('config', {})]
            },
            'json_renderer': {'item': 'watson.mvc.views.JsonRenderer'},
            'xml_renderer': {'item': 'watson.mvc.views.XmlRenderer'}
        }
    },
    'views': {
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
    },
    'events': {
        ROUTE_MATCH_EVENT: [('route_listener',)],
        DISPATCH_EXECUTE_EVENT: [('controller_dispatch_listener',)],
        RENDER_EVENT: [('render_listener',)],
        EXCEPTION_EVENT: [('exception_listener',)],
    }
}


class BaseApplication(ContainerAware, EventDispatcherAware):
    """
    The core application structure used for both WSGI and console based
    applications.
    It makes heavy use of the IocContainer and EventDispatcher classes to handle
    the wiring and executing of methods.
    """
    _config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = dict_deep_update(DEFAULTS, config or {})
        self.container.add('application.config', self.config)

    @property
    def container(self):
        if not self._container:
            self.container = IocContainer(self.config['dependencies'])
        return self._container

    @container.setter
    def container(self, container):
        container.add('application', self)
        self._container = container

    def __init__(self, config=None):
        self.config = config or {}
        self.dispatcher = self.container.get('shared_event_dispatcher')
        for event, listeners in self.config['events'].items():
            for callback_priority_pair in listeners:
                priority = callback_priority_pair[1] if len(callback_priority_pair) > 1 else 1
                self.dispatcher.add(event, self.container.get(callback_priority_pair[0]), priority)

    def __call__(self):
        raise NotImplementedError('You must implement __call__')


class WsgiApplication(BaseApplication):
    """
    An application structure suitable for use with the WSGI protocol.

    Usage:
        application = WsgiApplication({..})
        application(environ, start_response)
    """
    def __init__(self, config=None):
        super(WsgiApplication, self).__init__(config)

    def __call__(self, environ, start_response):
        request = create_request_from_environ(environ)
        route_event = Event(ROUTE_MATCH_EVENT, target=self, params={
            'request': request
        })
        try:
            route_event.params['router'] = self.container.get('router')
            route_result = self.dispatcher.trigger(route_event)
            dispatch_event = Event(DISPATCH_EXECUTE_EVENT, target=self, params={
                'route_match': route_result.first(),
                'request': request
            })
            dispatch_result = self.dispatcher.trigger(dispatch_event)
            response = dispatch_event.params['controller_class'].response
            view_model = dispatch_result.first()
        except ApplicationError as e:
            exception_event = Event(EXCEPTION_EVENT, target=self, params={
                'exception': e,
                'request': request
            })
            exception_result = self.dispatcher.trigger(exception_event)
            response = Response(e.status_code)
            view_model = exception_result.first()
        render_event = Event(RENDER_EVENT, target=self, params={
            'response': response,
            'view_model': view_model
        })
        self.dispatcher.trigger(render_event)
        start_response(*response.start())
        return [response()]


class ConsoleApplication(BaseApplication):
    """
    An application structure suitable for the command line.
    """
    # todo
