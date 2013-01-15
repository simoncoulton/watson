# -*- coding: utf-8 -*-
from watson.di import ContainerAware
from watson.di.container import IocContainer
from watson.events.dispatcher import EventDispatcherAware
from watson.http.messages import create_request_from_environ
from watson.stdlib.datastructures import dict_deep_update


ROUTE_MATCH_EVENT = 'event.application.route.match'
DISPATCH_EXECUTE_EVENT = 'event.application.dispatch.execute'
DEFAULTS = {
    'dependencies': {
        'definitions': {
            'shared_event_dispatcher': {
                'item': 'watson.events.dispatcher.EventDispatcher'
            }
        }
    },
    'events': {
        ROUTE_MATCH_EVENT: [],
        DISPATCH_EXECUTE_EVENT: []
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
        self.container.add('application.config', config)

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
    An application structure suitable for use within the WSGI protocol.

    Usage:
        application = WsgiApplication({..})
        application(environ, start_response)
    """
    def __init__(self, config=None):
        super(WsgiApplication, self).__init__(config)

    def __call__(self, environ, start_response):
        request = create_request_from_environ(environ)
        return request


class ConsoleApplication(BaseApplication):
    """
    An application structure suitable for the command line.
    """
