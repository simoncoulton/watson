# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse, ParseResult


class Url(object):
    """
    An object based representation of a Url.
    """
    @property
    def scheme(self):
        return self._parts.scheme

    @property
    def netloc(self):
        return self._parts.netloc

    @property
    def hostname(self):
        return self._parts.hostname

    @property
    def subdomain(self):
        """
        Returns the subdomain for the URL.
        With thanks: http://stackoverflow.com/questions/1189128/regex-to-extract-subdomain-from-url
        """
        regex = r'(?:http[s]*\:\/\/)*(.*?)\.(?=[^\/]*\..{2,5})'
        matches = re.match(regex, self.hostname)
        return matches.group(1) if matches else None

    @property
    def port(self):
        return self._parts.port

    @property
    def path(self):
        return self._parts.path

    def path_index(self, index=0):
        try:
            split_path = self.path.strip('/').split('/')
            return split_path[index]
        except:
            return None

    @property
    def params(self):
        return self._parts.params

    @property
    def query(self):
        return self._parts.query

    @property
    def fragment(self):
        return self._parts.fragment

    @property
    def username(self):
        return self._parts.username

    @property
    def password(self):
        return self._parts.password

    def __init__(self, url):
        """
        Create a new Url object from either a well formed url string,
        a dict of key/values, or a ParseResult.
        """
        if isinstance(url, ParseResult):
            self._parts = url
        elif isinstance(url, dict):
            if 'hostname' in url and 'netloc' not in url:
                netloc = url['hostname']
                if 'port' in url:
                    netloc += ':' + str(url['port'])
                url['netloc'] = netloc
                del url['hostname']
                del url['port']
            if 'params' not in url:
                url['params'] = None
            if 'fragment' not in url:
                url['fragment'] = None
            if 'path' not in url:
                url['path'] = None
            if 'query' not in url:
                url['query'] = None
            self._parts = ParseResult(**url)
        elif isinstance(url, str):
            self._parts = urlparse(url)

    def assemble(self):
        return self._parts.geturl()

    def __str__(self):
        return self.assemble()
