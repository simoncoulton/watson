# -*- coding: utf-8 -*-
from wsgiref import util
from nose.tools import raises
from watson.events.types import Event
from watson.http.messages import create_request_from_environ
from watson.mvc.routing import Router, RouteMatch
from watson.mvc.exceptions import NotFoundError
from watson.mvc.listeners import BaseListener, DispatchExecuteListener, ExceptionListener, RouteListener, RenderListener


class TestBaseListener(object):
    @raises(NotImplementedError)
    def test_missing_call(self):
        listener = BaseListener()
        listener('test')


class TestRouteListener(object):
    def create_event(self, **kwargs):
        router = Router({'home': {'path': '/'}})
        environ = {}
        util.setup_testing_defaults(environ)
        environ.update(**kwargs)
        event = Event('TestEvent', params={'router': router, 'request': create_request_from_environ(environ)})
        return event

    def test_response(self):
        listener = RouteListener()
        result = listener(self.create_event())
        assert isinstance(result, RouteMatch)

    @raises(NotFoundError)
    def test_not_found(self):
        listener = RouteListener()
        listener(self.create_event(PATH_INFO='/test'))


class TestDispatchExecuteListener(object):
    pass


class TestExceptionListener(object):
    pass


class TestRenderListener(object):
    pass
