# -*- coding: utf-8 -*-
from wsgiref import util
from nose.tools import raises
from watson.http.messages import create_request_from_environ
from watson.mvc.routing import create_route_from_definition
from watson.mvc.routing import StaticRoute, SegmentRoute, Router

sample_routes = {
    'home': {
        'path': '/',
        'accepts': ('GET',)
    },
    'dump': {
        'path': '/dump',
        'requires': {
            'format': 'json'
        }
    },
    'dump_format_segment_requires': {
        'path': '/dump.:format',
        'type': 'segment',
        'requires': {
            'format': 'json'
        }
    },
    'dump_format_segment_optional': {
        'path': '/dump[.:format]',
        'type': 'segment',
    },
    'edit_user': {
        'path': '/edit/:id',
        'type': 'segment'
    },
    'search': {
        'path': '/search[/:keyword]',
        'type': 'segment',
        'defaults': {
            'keyword': 'blah'
        }
    },
    'subdomain': {
        'path': '/subdomain/:sub',
        'type': 'segment',
        'subdomain': 'clients'
    }
}


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


class TestRouting(object):
    def test_create_route_from_definition(self):
        segment_route = {
            'path': '/',
            'type': 'SegmentRoute'
        }
        static_route = {
            'path': '/'
        }
        assert isinstance(create_route_from_definition('home', segment_route), SegmentRoute)
        assert isinstance(create_route_from_definition('home', static_route), StaticRoute)


class TestRouter(object):
    def test_create_router(self):
        router = Router(sample_routes)
        assert router.__repr__() == '<watson.mvc.routing.Router routes:{0}>'.format(len(sample_routes))

    def test_matches(self):
        router = Router(sample_routes)
        request = create_request_from_environ(sample_environ(PATH_INFO='/'))
        matches = router.matches(request)
        assert len(matches) == 1
        assert matches[0].name == 'home'
        assert matches[0].__repr__() == '<watson.mvc.routing.RouteMatch name:home>'


class TestStaticRoute(object):
    def test_create_static_route(self):
        route = StaticRoute({'path': '/'})
        assert route.__repr__() == '<watson.mvc.routing.StaticRoute path:/>'

    def test_static_match(self):
        route = StaticRoute({'path': '/dump'})
        request = create_request_from_environ(sample_environ(PATH_INFO='/dump'))
        matched, params = route.match(request)
        assert matched == True


class TestSegmentRoute(object):
    def test_covert_segment_to_regex(self):
        route = SegmentRoute({'name': 'home', 'path': '/:test'})
        assert route.regex.pattern == '\/(?P<test>[^/]+)'
        assert route.name == 'home'
        assert route.__repr__() == '<watson.mvc.routing.SegmentRoute path:\/(?P<test>[^/]+)>'

    def test_convert_segment_to_regex_optional(self):
        route = SegmentRoute({'path': '/[:test]'})
        assert route.regex.pattern == '\/(?:(?P<test>[^/]+))?'

    def test_match_pattern(self):
        route = SegmentRoute(sample_routes['search'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/search/my-term'))
        matched, params = route.match(request)
        assert matched == True
        assert params['keyword'] == 'my-term'

    def test_accept_method(self):
        route = SegmentRoute(sample_routes['home'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/', REQUEST_METHOD='POST'))
        matched, params = route.match(request)
        assert matched == False

    def test_subdomain(self):
        route = SegmentRoute(sample_routes['subdomain'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/subdomain/test', REQUEST_METHOD='POST', SERVER_NAME='clients.test.com'))
        matched, params = route.match(request)
        assert matched == True

    def test_format_accept(self):
        route = SegmentRoute(sample_routes['dump'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/dump', HTTP_ACCEPT='application/json'))
        matched, params = route.match(request)
        assert matched == True

    def test_format_accept_invalid(self):
        route = SegmentRoute(sample_routes['dump'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/dump', HTTP_ACCEPT='application/xml'))
        matched, params = route.match(request)
        assert matched == False

    def test_format_segment_requires(self):
        route = SegmentRoute(sample_routes['dump_format_segment_requires'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/dump.json'))
        matched, params = route.match(request)
        assert matched == True

    def test_format_segment_optional(self):
        route = SegmentRoute(sample_routes['dump_format_segment_optional'])
        request = create_request_from_environ(sample_environ(PATH_INFO='/dump.xml'))
        matched, params = route.match(request)
        assert matched == True
        assert params['format'] == 'xml'

    @raises(ValueError)
    def test_bracket_mismatch(self):
        SegmentRoute({'path': '/[test]]'})
