# -*- coding: utf-8 -*-
from urllib.parse import urlparse, ParseResult
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
        parsed_url = urlparse('http://simon:test@www.google.com:80/path/path2?q=test#frag')
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
