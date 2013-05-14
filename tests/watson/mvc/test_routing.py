# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.http.messages import create_request_from_environ
from watson.mvc.routing import Route, Router
from tests.watson.mvc.support import sample_environ


class TestRoute(object):
    def test_create_route(self):
        route = Route(name='home', path='/')
        assert route.path == '/'
        assert route.name == 'home'
        assert repr(route) == '<watson.mvc.routing.Route name:home path:/ match:\/$>'

    def test_create_route_regex(self):
        route = Route(name='home', path='/', regex='.*')
        assert route.regex

    def test_static_match(self):
        route = Route(name='home', path='/')
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/test'))
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/'))
        assert not route.match(invalid_request).matched
        assert route.match(valid_request).matched

    def test_optional_segment_match(self):
        route = Route(name="search", path='/search[/:keyword]')
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/searching'))
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/search'))
        valid_request_with_param = create_request_from_environ(sample_environ(PATH_INFO='/search/test'))
        assert not route.match(invalid_request).matched
        assert route.match(valid_request).matched
        assert route.match(valid_request_with_param).matched

    def test_optional_segment_with_defaults(self):
        route = Route(name="search", path='/search[/:keyword]', defaults={'keyword': 'blah'})
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/searching'))
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/search'))
        valid_request_with_param = create_request_from_environ(sample_environ(PATH_INFO='/search/test'))
        valid_request_with_default = route.match(valid_request)
        assert not route.match(invalid_request).matched
        assert valid_request_with_default.matched
        assert valid_request_with_default.params == {'keyword': 'blah'}
        assert route.match(valid_request_with_param).matched

    def test_optional_segment_with_required(self):
        route = Route(name="search", path='/search[/:keyword]', requires={'keyword': 'blah'})
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/search/blah'))
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/search/test'))
        assert not route.match(invalid_request).matched
        assert route.match(valid_request).matched

    def test_mandatory_segment_match(self):
        route = Route("search", path='/search/:keyword')
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/searching'))
        valid_request_no_param = create_request_from_environ(sample_environ(PATH_INFO='/search'))
        valid_request_with_param = create_request_from_environ(sample_environ(PATH_INFO='/search/test'))
        assert not route.match(invalid_request).matched
        assert not route.match(valid_request_no_param).matched
        assert route.match(valid_request_with_param).matched

    @raises(ValueError)
    def test_segment_bracket_mismatch(self):
        Route(name='mismatch', path='/search:keyword]')

    def test_format_match(self):
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/dump', HTTP_ACCEPT='application/json'))
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/dump', HTTP_ACCEPT='application/xml'))
        valid_request_segment = create_request_from_environ(sample_environ(PATH_INFO='/dump.json'))
        route = Route(name='json', path='/dump', requires={'format': 'json'})
        route_format = Route(name='json', path='/dump.:format', requires={'format': 'json'})
        assert route.match(valid_request).matched
        assert not route.match(invalid_request).matched
        assert route_format.match(valid_request_segment).matched

    def test_accept_method_match(self):
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/test', REQUEST_METHOD='POST'))
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/test', REQUEST_METHOD='GET'))
        route = Route(name='test', path='/test', accepts=('POST',))
        assert route.match(valid_request).matched
        assert not route.match(invalid_request).matched

    def test_subdomain_match(self):
        valid_request = create_request_from_environ(sample_environ(PATH_INFO='/test', SERVER_NAME='clients.test.com'))
        invalid_request = create_request_from_environ(sample_environ(PATH_INFO='/test', SERVER_NAME='clients2.test.com'))
        route = Route(name='test', path='/test', subdomain='clients')
        assert route.match(valid_request).matched
        assert not route.match(invalid_request).matched

    def test_assemble_static_route(self):
        route = Route(name='test', path='/testing')
        assert route.assemble() == '/testing'

    def test_assemble_segment_route(self):
        route = Route(name='test', path='/search[/:keyword]')
        assert route.assemble(keyword='test') == '/search/test'

    @raises(KeyError)
    def test_assemble_segment_route_missing_param(self):
        route = Route(name='test', path='/search/:keyword')
        route.assemble()


class TestRouter(object):
    def test_create_from_dict(self):
        router = Router({
            'home': {
                'path': '/'
            }
        })
        assert len(router) == 1
        router_objects = Router({
            'home': Route(name='home', path='/')
        })
        assert len(router_objects) == 1
        for route in router:
            assert True
        assert router.assemble('home') == '/'
        assert repr(router) == '<watson.mvc.routing.Router routes:1>'

    def test_create_from_list(self):
        router = Router([
            {
                'name': 'home',
                'path': '/'
            }
        ])
        assert len(router) == 1
        router_objects = Router([
            Route(name='home', path='/')
        ])
        assert len(router_objects) == 1

    @raises(KeyError)
    def test_assemble_invalid_route(self):
        router = Router()
        router.assemble('test')

    def test_sort_routes(self):
        router = Router({
            'home': {
                'path': '/'
            },
            'test': {
                'path': '/'
            },
            'highest': {
                'path': '/',
                'priority': 1000
            },
            'lowest': {
                'path': '/',
                'priority': -1
            }
        })
        request = create_request_from_environ(sample_environ(PATH_INFO='/'))
        matches = router.matches(request)
        assert matches[0].route.name == 'highest'
        assert matches[3].route.name == 'lowest'
