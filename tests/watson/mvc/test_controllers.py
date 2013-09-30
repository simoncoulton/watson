# -*- coding: utf-8 -*-
from io import BytesIO, BufferedReader
from nose.tools import raises
from unittest.mock import Mock
from watson.events import types
from watson.http.messages import Request, Response, create_request_from_environ
from watson.mvc import controllers
from watson.mvc.routing import Router
from tests.watson.mvc.support import SampleActionController, SampleRestController, sample_environ


class TestNotImplementedController(object):

    @raises(TypeError)
    def test_execute_invalid(self):
        controllers.Base()


class TestBaseHttpController(object):

    def test_request_response(self):
        base = controllers.HttpMixin()
        base.request = Request('GET')
        assert isinstance(base.request, Request)
        assert isinstance(base.response, Response)

    def test_get_event(self):
        base = controllers.HttpMixin()
        base.event = types.Event('test')
        assert isinstance(base.event, types.Event)

    @raises(TypeError)
    def test_set_event(self):
        base = controllers.HttpMixin()
        base.event = 'test'

    @raises(TypeError)
    def test_invalid_request(self):
        base = controllers.HttpMixin()
        base.request = 'test'

    @raises(TypeError)
    def test_invalid_response(self):
        base = controllers.HttpMixin()
        base.response = 'test'

    def test_route_to_url(self):
        base = controllers.HttpMixin()
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
        assert base.url('segment', part='test') == '/segment/test'
        assert base.url('test', host='test.com') == 'test.com/test'
        assert base.url('test', host='test.com', scheme='https://') == 'https://test.com/test'

    def test_redirect(self):
        base = controllers.HttpMixin()
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
        base.request = create_request_from_environ(sample_environ())
        base.container = Mock()
        base.container.get.return_value = router
        response = base.redirect('/test')
        assert response.headers['location'] == '/test'
        response = base.redirect('segment')
        assert response.headers['location'] == '/segment/test'
        assert response.status_code == 302

    def test_post_redirect_get(self):
        base = controllers.HttpMixin()
        router = Router({'test': {'path': '/test'}})
        environ = sample_environ(PATH_INFO='/', REQUEST_METHOD='POST')
        environ['wsgi.input'] = BufferedReader(
            BytesIO(b'post_var_one=test&post_var_two=blah'))
        base.request = create_request_from_environ(
            environ, 'watson.http.sessions.Memory')
        base.container = Mock()
        base.container.get.return_value = router
        response = base.redirect('test')
        assert response.status_code == 303
        assert base.redirect_vars == base.request.session['post_redirect_get']
        base.clear_redirect_vars()
        assert not base.redirect_vars
        base.redirect('test', clear=True)
        assert not base.redirect_vars

    def test_flash_message(self):
        controller = SampleActionController()
        controller.request = Request('GET')
        controller.flash_messages.add('testing')
        controller.flash_messages.add('something')
        assert controller.flash_messages['info'] == ['testing', 'something']
        for namespace, message in controller.flash_messages:
            assert namespace == 'info'
        assert not controller.flash_messages.messages


class TestActionController(object):

    def test_repr(self):
        controller = SampleActionController()
        assert repr(
            controller) == '<tests.watson.mvc.support.SampleActionController>'

    def test_execute_result(self):
        controller = SampleActionController()
        assert controller.execute(action='something') == 'something_action'
        assert controller.execute(action='blah') == 'blah_action'

    def test_method_template(self):
        controller = SampleActionController()
        assert controller.get_execute_method_path(
            action='something') == ['sampleactioncontroller', 'something']


class TestRestController(object):

    def test_execute_result(self):
        controller = SampleRestController()
        controller.request = Request('GET')
        result = controller.execute(something='test')
        assert result == 'GET'

    def test_method_template(self):
        controller = SampleRestController()
        controller.request = Request('GET')
        assert controller.get_execute_method_path() == [
            'samplerestcontroller', 'get']


class TestFlashMessageContainer(object):

    def test_create(self):
        session_data = {}
        container = controllers.FlashMessagesContainer(session_data)
        assert len(container) == 0
        assert repr(
            container) == '<watson.mvc.controllers.FlashMessagesContainer messages: 0>'

    def test_add_messages(self):
        session_data = {}
        container = controllers.FlashMessagesContainer(session_data)
        container.add_messages(['testing'])
        assert len(container) == 1

    def test_set_existing_container(self):
        existing_container = controllers.FlashMessagesContainer({})
        existing_container.add('Test')
        session_data = {'flash_messages': existing_container}
        new_container = controllers.FlashMessagesContainer(session_data)
        assert len(new_container) == 1
