# -*- coding: utf-8 -*-
from wsgiref import util
from nose.tools import raises
from watson.di.container import IocContainer
from watson.events.types import Event
from watson.http.messages import create_request_from_environ, Response
from watson.mvc.routing import Router, RouteMatch, Route
from watson.mvc.exceptions import NotFoundError, InternalServerError
from watson.mvc import listeners
from tests.watson.mvc.support import sample_environ


class TestBaseListener(object):

    @raises(TypeError)
    def test_missing_call(self):
        listeners.Base()


class TestRouteListener(object):

    def create_event(self, **kwargs):
        router = Router({'home': {'path': '/'}})
        environ = {}
        util.setup_testing_defaults(environ)
        environ.update(**kwargs)
        event = Event(
            'TestEvent',
            params={'router': router,
                    'request': create_request_from_environ(environ)})
        return event

    def test_response(self):
        listener = listeners.Route()
        result = listener(self.create_event())
        assert isinstance(result, RouteMatch)

    @raises(NotFoundError)
    def test_not_found(self):
        listener = listeners.Route()
        listener(self.create_event(PATH_INFO='/test'))


class TestDispatchExecuteListener(object):

    @raises(InternalServerError)
    def test_execute(self):
        route = Route('test', path='/')
        match = RouteMatch(route, {})
        event = Event('something', params={'route_match': match})
        listener = listeners.DispatchExecute({'404': 'page/404'})
        listener(event)

    def test_short_circuit(self):
        environ = sample_environ()
        route = Route(
            'test',
            path='/',
            options={'controller': 'tests.watson.mvc.support.ShortCircuitedController'})
        match = RouteMatch(
            route,
            {'controller': 'tests.watson.mvc.support.ShortCircuitedController'})
        event = Event(
            'something',
            params={'route_match': match,
                    'container': IocContainer(),
                    'request': create_request_from_environ(environ)})
        listener = listeners.DispatchExecute({'404': 'page/404'})
        response = listener(event)
        assert isinstance(response, Response)


class TestExceptionListener(object):
    pass


class TestRenderListener(object):
    pass
