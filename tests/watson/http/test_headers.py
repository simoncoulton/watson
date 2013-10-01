# -*- coding: utf-8 -*-
from watson.http.headers import HeaderDict, parse_to_environ_header_field, parse_from_environ_header_field


class TestHeaders(object):

    def test_add_header(self):
        d = HeaderDict()
        d.add('CONTENT_TYPE', 'text/html')
        assert d.get('Content-Type') == 'text/html'
        assert d.get('CONTENT_TYPE') == 'text/html'

    def test_add_option(self):
        d = HeaderDict()
        d.add('CONTENT_TYPE', 'text/html', charset='utf-8')
        assert d.get('Content-Type') == 'text/html; charset=utf-8'
        assert d.get_option('Content-Type', 'charset') == 'utf-8'
        assert d.get_option('Content-Type', 'random', 'test') == 'test'

    def test_add_overwrite_header(self):
        d = HeaderDict()
        d.add('CONTENT_TYPE', 'text/html', charset='utf-8')
        assert len(d) == 1
        d.add('CONTENT_TYPE', 'text/plain', charset='utf-8', replace=True)
        assert len(d) == 1

    def test_delete_header(self):
        d = HeaderDict()
        d['Content-Type'] = 'test'
        d['Test'] = 'test'
        assert d.get('Content-Type')
        del d['Content-Type']
        assert not d.get('Content-Type')

    def test_tuple_pairs(self):
        d = HeaderDict({'Content-Type': 'text/html'})
        assert d() == [('Content-Type', 'text/html')]

    def test_tuple_pairs_multiple(self):
        d = HeaderDict({'Content-Type': 'text/html'})
        d.add('Content-Type', 'text/xml')
        assert d() == [
            ('Content-Type', 'text/html'), ('Content-Type', 'text/xml')]


class TestModuleFunctions(object):

    def test_parse_to_environ(self):
        assert parse_to_environ_header_field('Content-Type') == 'CONTENT_TYPE'

    def test_parse_from_environ(self):
        assert parse_from_environ_header_field(
            'CONTENT_TYPE') == 'Content-Type'
