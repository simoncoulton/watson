# -*- coding: utf-8 -*-
from nose.tools import raises
from unittest.mock import Mock
from watson.http.messages import Request, Response
from watson.mvc.controllers import BaseController, HttpControllerMixin
from watson.mvc.routing import Router
from tests.watson.mvc.support import SampleActionController, SampleRestController


class TestNotImplementedController(object):
    @raises(NotImplementedError)
    def test_execute_invalid(self):
        base = BaseController()
        base.execute()

    @raises(NotImplementedError)
    def test_method_template_invalid(self):
        base = BaseController()
        base.get_execute_method_path()


class TestBaseHttpController(object):
    def test_request_response(self):
        base = HttpControllerMixin()
        base.request = Request('GET')
        assert isinstance(base.request, Request)
        assert isinstance(base.response, Response)
        assert repr(base) == '<watson.mvc.controllers.HttpControllerMixin>'

    @raises(TypeError)
    def test_invalid_request(self):
        base = HttpControllerMixin()
        base.request = 'test'

    @raises(TypeError)
    def test_invalid_response(self):
        base = HttpControllerMixin()
        base.response = 'test'

    def test_route_to_url(self):
        base = HttpControllerMixin()
        router = Router({
            'test': {
                'path': '/test',
            },
            'segment': {
                'path': '/segment[/:part]',
                'type': 'segment'
            }
        })
        base.container = Mock()
        base.container.get.return_value = router
        assert base.url('test') == '/test'
        assert base.url('segment', {'part': 'test'}) == '/segment/test'

    def test_redirect(self):
        base = HttpControllerMixin()
        router = Router({
            'test': {
                'path': '/test',
            },
            'segment': {
                'path': '/segment[/:part]',
                'type': 'segment',
                'defaults': {'part': 'test'}
            }
        })
        base.container = Mock()
        base.container.get.return_value = router
        response = base.redirect('/test', is_url=True)
        assert response.headers['location'] == '/test'
        response = base.redirect('segment')
        assert response.headers['location'] == '/segment/test'
        assert response.status_code == 302


class TestActionController(object):
    def test_execute_result(self):
        controller = SampleActionController()
        assert controller.execute(action='something') == 'something_action'
        assert controller.execute(action='blah') == 'blah_action'

    def test_method_template(self):
        controller = SampleActionController()
        assert controller.get_execute_method_path(action='something') == ['sampleactioncontroller', 'something']


class TestRestController(object):
    def test_execute_result(self):
        controller = SampleRestController()
        controller.request = Request('GET')
        result = controller.execute(something='test')
        assert result == 'GET'

    def test_method_template(self):
        controller = SampleRestController()
        controller.request = Request('GET')
        assert controller.get_execute_method_path() == ['samplerestcontroller', 'get']
