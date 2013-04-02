# -*- coding: utf-8 -*-
import re
from watson.http import REQUEST_METHODS, MIME_TYPES
from watson.common.imports import get_qualified_name


def create_route_from_definition(name, definition):
    definition['name'] = name
    return StaticRoute(definition) if definition.get('type', 'StaticRoute') == 'StaticRoute' else SegmentRoute(definition)


class Router(object):
    _routes = None

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, routes):
        self._routes = {name: create_route_from_definition(name, definition) for name, definition in routes.items()}

    def __init__(self, routes=None):
        self.routes = routes or {}

    def matches(self, request):
        matches = []
        for name, route in self.routes.items():
            matched, params = route.match(request)
            if matched:
                matches.append(RouteMatch(route, params))
        return matches

    def assemble(self, route_name, **kwargs):
        if route_name in self.routes:
            return self.routes[route_name].assemble(**kwargs)
        else:
            raise Exception('No route named {0} can be found.'.format(route_name))

    def __repr__(self):
        return '<{0} routes:{1}>'.format(get_qualified_name(self), len(self.routes))


class RouteMatch(object):
    route = None
    params = None

    @property
    def name(self):
        return self.route.name

    def __init__(self, route, params=None):
        self.route = route
        self.params = params or {}

    def __repr__(self):
        return '<{0} name:{1}>'.format(get_qualified_name(self), self.name)


class BaseRoute(dict):
    @property
    def name(self):
        return self['name']

    def __init__(self, *args, **kwargs):
        super(BaseRoute, self).__init__(*args, **kwargs)
        if 'format' in self.get('requires', ()):
            self['format'] = re.compile(self['requires']['format'])

    def match(self, request):
        matched = True
        params = self.get('defaults', {}).copy()
        if request.method not in self.get('accepts', REQUEST_METHODS):
            matched = False
        if 'subdomain' in self and request.url.subdomain != self.get('subdomain'):
            matched = False
        accept_format = request.headers.get('Accept')
        formats = None
        if accept_format:
            formats = [format for format in MIME_TYPES if
                        accept_format in MIME_TYPES[format]]
            if formats:
                params['format'] = formats[0]
        if 'format' in self and formats:
            if self['format'].match(formats[0]):
                params['format'] = formats[0]
            else:
                matched = False
        return matched, params


class SegmentRoute(BaseRoute):
    regex = None
    segments = None

    def __init__(self, *args, **kwargs):
        super(SegmentRoute, self).__init__(*args, **kwargs)
        if not self.regex:
            self.regex, self.segments = self.__create_regex_from_segment_path(self['path'], self.get('requires', {}))

    def match(self, request):
        matched, params = super(SegmentRoute, self).match(request)
        if matched:
            matches = self.regex.match(request.url.path)
            if not matches:
                matched = False
            else:
                params.update((k, v) for k, v in matches.groupdict().items() if v is not None)
        return matched, params

    def assemble(self, **kwargs):
        params = kwargs or {}
        params.update(self.get('defaults', {}))
        return ''.join(self.__build_path(self.segments, params))

    def __build_path(self, segments, params):
        path = []
        for segment in segments:
            if isinstance(segment[1], list):
                path.append(self.__build_path(segment[1], params))
            else:
                value = segment[1]
                if segment[0] == 'param':
                    value = params.get(value)
                    if value:
                        path.append(str(value))
                    else:
                        raise KeyError('Missing {0} in params.'.format(segment[1]))
                else:
                    path.append(segment[1])
        return ''.join(path)

    def __create_regex_from_segment_path(self, path, requires=None):
        """
        Converts a segemented path into a regular expression. Inspired by Rails
        and ZF2.

        Args:
            path: the segmented path to convert to regex
            requires: a dict of required values for any optional segments

        Returns:
            SRE_Pattern for the segment
        """
        start, path_length, depth, segments = 0, len(path), 0, []
        depth_segments = [segments]
        pattern = re.compile('(?P<static>[^:\[\]]*)(?P<token>[:\[\]]|$)')
        token_pattern = re.compile('(?P<name>[^:/\[\]]+)')
        while start < path_length:
            matches = pattern.search(path, start)
            offset = '{0}{1}'.format(matches.groups()[0], matches.groups()[1])
            start += len(offset)
            token = matches.group('token')
            static_part = matches.group('static')
            if static_part:
                depth_segments[depth].append(('static', static_part))
            if token == ':':
                token_matches = token_pattern.search(path, start)
                param = token_matches.groupdict()['name']
                depth_segments[depth].append(('param', param))
                start += len(param)
            elif token == '[':
                depth += 1
                current_depth = depth - 1
                total_depths = len(depth_segments)
                if total_depths <= depth:
                    depth_segments.append([])
                depth_segments[current_depth].append(('optional', []))
                depth_segments[depth] = depth_segments[current_depth][len(depth_segments[current_depth]) - 1][1]
            elif token == ']':
                del depth_segments[depth]
                depth -= 1
                if depth < 0:
                    raise ValueError('Bracket mismatch detected.')
            else:
                break
        del depth_segments
        return re.compile(self.__convert_hierarchy_to_regex(segments, requires)), segments

    def __convert_hierarchy_to_regex(self, hierarchy, requires):
        _regex = []
        for _type, value in hierarchy:
            if _type == 'static':
                _regex.append(re.escape(value))
            elif _type == 'optional':
                _regex.append(
                    '(?:{0})?'.format(self.__convert_hierarchy_to_regex(value, requires)))
            else:
                _regex.append(
                    '(?P<{0}>{1})'.format(value, requires.get(value, '[^/]+')))
        return ''.join(_regex)

    def __repr__(self):
        return '<{0} path:{1}>'.format(get_qualified_name(self), self.regex.pattern)


class StaticRoute(BaseRoute):
    def match(self, request):
        matched, params = super(StaticRoute, self).match(request)
        if matched:
            matched = request.url.path == self['path']
        return matched, params

    def assemble(self, **kwargs):
        return self['path']

    def __repr__(self):
        return '<{0} path:{1}>'.format(get_qualified_name(self), self['path'])
