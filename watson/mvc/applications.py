# -*- coding: utf-8 -*-
import os
from types import ModuleType
from watson.di import ContainerAware
from watson.di.container import IocContainer
from watson.events.dispatcher import EventDispatcherAware
from watson.events.types import Event
from watson.http.messages import create_request_from_environ, Response
from watson.mvc.exceptions import ApplicationError
from watson.stdlib.datastructures import dict_deep_update, module_to_dict


INIT_EVENT = 'event.mvc.init'
ROUTE_MATCH_EVENT = 'event.mvc.route.match'
DISPATCH_EXECUTE_EVENT = 'event.mvc.dispatch.execute'
RENDER_VIEW_EVENT = 'event.mvc.render.view'
EXCEPTION_EVENT = 'event.mvc.exception'
DEFAULTS = {
    'debug': {
        'profiling': {
            'enabled': False,
            'max_results': 20,
            'sort': 'cumulative',
        }
    },
    'dependencies': {
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
        EXCEPTION_EVENT: [('watson.mvc.listeners.ExceptionListener',)],
        INIT_EVENT: [
            ('watson.debug.profilers.ApplicationInitListener', 1, True)
        ],
        ROUTE_MATCH_EVENT: [('watson.mvc.listeners.RouteListener',)],
        DISPATCH_EXECUTE_EVENT: [('watson.mvc.listeners.DispatchExecuteListener',)],
        RENDER_VIEW_EVENT: [('watson.mvc.listeners.RenderListener',)],
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
        if isinstance(config, ModuleType):
            conf = module_to_dict(config, '__')
        else:
            conf = config or {}
        self._config = dict_deep_update(DEFAULTS, conf)
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
                try:
                    priority = callback_priority_pair[1]
                except:
                    priority = 1
                try:
                    once_only = callback_priority_pair[2]
                except:
                    once_only = False
                self.dispatcher.add(event, self.container.get(callback_priority_pair[0]), priority, once_only)
        self.dispatcher.trigger(Event(INIT_EVENT, target=self))

    def __call__(self):
        raise NotImplementedError('You must implement __call__')


class HttpApplication(BaseApplication):
    """
    An application structure suitable for use with the WSGI protocol.

    Usage:
        application = HttpApplication({..})
        application(environ, start_response)
    """
    def run(self, environ, start_response):
        request = create_request_from_environ(environ)
        try:
            route_result = self.dispatcher.trigger(Event(ROUTE_MATCH_EVENT, target=self, params={
                'request': request,
                'router': self.container.get('router')
            }))
            route_match = route_result.first()
        except ApplicationError as exc:
            route_match = None
            response, view_model = self.__raise_exception_event(exception=exc, request=request)
        if route_match:
            try:
                dispatch_event = Event(DISPATCH_EXECUTE_EVENT, target=self, params={
                    'route_match': route_match,
                    'request': request
                })
                dispatch_result = self.dispatcher.trigger(dispatch_event)
                response = dispatch_event.params['controller_class'].response
                view_model = dispatch_result.first()
            except ApplicationError as exc:
                response, view_model = self.__raise_exception_event(exception=exc, request=request, route_match=route_match)
        try:
            self.__render(request=request, response=response, view_model=view_model)
        except ApplicationError as exc:
            response, view_model = self.__raise_exception_event(exception=exc, request=request, route_match=route_match)
            self.__render(request=request, response=response, view_model=view_model)
        start_response(*response.start())
        return [response()]

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __raise_exception_event(self, **kwargs):
        exception_event = Event(EXCEPTION_EVENT, target=self, params=kwargs)
        exception_result = self.dispatcher.trigger(exception_event)
        return Response(kwargs['exception'].status_code), exception_result.first()

    def __render(self, **kwargs):
        render_event = Event(RENDER_VIEW_EVENT, target=self, params=kwargs)
        self.container.add('render_event_params', kwargs)
        self.dispatcher.trigger(render_event)


class ConsoleApplication(BaseApplication):
    """
    An application structure suitable for the command line.
    """
    # todo
