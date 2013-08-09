# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from watson.http.uri import Url


class TestUrl(object):

    def test_create_from_string(self):
        url = Url('http://simon:test@www.google.com:80/path/path2?q=test#frag')
        assert url.scheme == 'http'
        assert url.hostname == 'www.google.com'
        assert url.subdomain == 'www'
        assert url.fragment == 'frag'
        assert url.port == 80
        assert url.path == '/path/path2'
        assert url.path_index(0) == 'path'
        assert url.query == 'q=test'
        assert url.username == 'simon'
        assert url.password == 'test'
        assert url.netloc == 'simon:test@www.google.com:80'

    def test_create_from_parse_result(self):
        parsed_url = urlparse(
            'http://simon:test@www.google.com:80/path/path2?q=test#frag')
        url = Url(parsed_url)
        assert url.scheme == 'http'
        assert url.hostname == 'www.google.com'
        assert url.subdomain == 'www'
        assert url.fragment == 'frag'
        assert url.port == 80
        assert url.path == '/path/path2'
        assert url.path_index(0) == 'path'
        assert url.query == 'q=test'
        assert url.username == 'simon'
        assert url.password == 'test'
        assert url.netloc == 'simon:test@www.google.com:80'

    def test_create_from_dict(self):
        url = Url({
            'scheme': 'http',
            'hostname': 'www.google.com',
            'fragment': 'frag',
            'port': 80,
            'path': '/path/path2',
            'query': 'q=test',
            'username': 'simon',
            'password': 'test'
        })
        assert url.scheme == 'http'
        assert url.hostname == 'www.google.com'
        assert url.subdomain == 'www'
        assert url.fragment == 'frag'
        assert url.port == 80
        assert url.path == '/path/path2'
        assert url.path_index(0) == 'path'
        assert url.query == 'q=test'
        assert url.netloc == 'simon:test@www.google.com:80'
        assert not url.path_index(4)

    def test_create_from_dict_empty(self):
        url = Url({
            'hostname': 'www.google.com'
        })
        assert not url.fragment
        assert url.path == '/'
        assert not url.query

    def test_params(self):
        url = Url('http://www.google.com/search;test=blah')
        assert url.params == 'test=blah'
