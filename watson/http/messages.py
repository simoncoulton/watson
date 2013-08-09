# -*- coding: utf-8 -*-
from copy import copy
from wsgiref.util import request_uri
from watson.common.datastructures import ImmutableMultiDict, MultiDict
from watson.common.imports import get_qualified_name
from watson.http import STATUS_CODES, REQUEST_METHODS
from watson.http.cookies import CookieDict
from watson.http.headers import HeaderDict, split_headers_server_vars
from watson.http.uri import Url
from watson.http.wsgi import get_form_vars
from watson.http.sessions import SessionMixin


class MessageMixin(object):

    """Base mixin for all Http Message objects.
    """
    _headers = None
    _version = None
    body = None

    @property
    def version(self):
        return self._version or '1.1'

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def headers(self):
        if not self._headers:
            self._headers = HeaderDict()
        return self._headers

    @headers.setter
    def headers(self, headers):
        if not isinstance(headers, HeaderDict):
            headers = HeaderDict(headers)
        self._headers = headers

    def __init__(self, headers=None, body=None):
        if headers:
            self.headers = headers
        self.body = body or ''


def create_request_from_environ(
        environ, session_class=None, session_options=None):
    """Create a new Request object.

    Create a new Request object based on a set of environ variables. To create
    a mutable version of the request you should copy() the Request object.

    If a POST variable named HTTP_REQUEST_METHOD is found, the Http Request
    method will be set to that method.
    """
    headers, server, cookies = split_headers_server_vars(environ)
    get, post, files = get_form_vars(environ)
    if post.get('HTTP_REQUEST_METHOD', '').upper() in REQUEST_METHODS:
        method = post.get('HTTP_REQUEST_METHOD')
    else:
        method = server['REQUEST_METHOD']
    request = Request(
        method, ImmutableMultiDict(get), ImmutableMultiDict(post),
        ImmutableMultiDict(files), ImmutableMultiDict(headers),
        ImmutableMultiDict(server), cookies)
    if session_class:
        request.define_session(session_class, session_options or {})
    return request


class Request(MessageMixin, SessionMixin):

    """
    Provides a simple and usable interface for dealing with Http Requests.
    Requests are designed to be immutable and not altered after they are
    created, as such you should only set get/post/cookie etc attributes via
    the __init__.
    By default the session storage method is MemoryStorage which will store
    session in ram.

    See:
        http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
        http://ken.coar.org/cgi/draft-coar-cgi-v11-03.txt

    Usage:
        request = create_request_from_environ(environ)
        print(request.method)
        print(request.post('my_post_var'))

        request = Request('get', {'get_var': 'somevalue'})
        print(request.method) # get
        print(request.get('get_var')) # somevalue
    """
    _method = None
    _url = None
    _get = None
    _post = None
    _files = None
    _headers = None
    _server = None
    _cookies = None

    @property
    def method(self):
        """The method associated with the request.

        Returns:
            A string representation of the Http Request method
        """
        return self._method.upper()

    @property
    def get(self):
        """A dict of all GET variables associated with the request.

        Returns:
            A dict of GET variables
        """
        return self._get

    @property
    def post(self):
        """A dict of all POST variables associated with the request.

        Returns:
            A dict of POST variables
        """
        return self._post

    @property
    def files(self):
        """A dict of all files that have been uploaded as part of a
        enctype="multipart/form-data" request.

        Usage:
            request = ...
            request.files['uploaded_file'] # FieldStorage object

        Returns:
            A dict of FieldStorage objects
        """
        return self._files

    @property
    def server(self):
        """A dict of all environ variables associated with the server where the
        request originated.

        Returns:
            A dict of environ variables
        """
        return self._server

    @property
    def cookies(self):
        """A dict of all cookies from the request.

        Usage:
            request = ...
            request.cookies.get('test') # value of cookie named 'test'

        Returns:
            A watson.http.cookies.CookieDict object
        """
        return self._cookies

    @property
    def url(self):
        """Generates a watson.http.uri.Url object based on Request.server variables.

        Usage:
            request = ...
            print(request.url.path) # /

        Returns:
            A watson.http.uri.Url object
        """
        if not self._url:
            self._url = Url(request_uri(self._server))
        return self._url

    def __init__(self, method, get=None, post=None, files=None, headers=None,
                 server=None, cookies=None, body=''):
        """Creates a new instance of the Request object.

        Args:
            method: The Http request method
            get: A watson.common.datastructures.MultiDict containing GET variables
            post: A watson.common.datastructures.MultiDict containing POST variables
            files: A watson.common.datastructures.MultiDict containing FieldStorage objects
            headers: A watson.http.headers.HeaderDict containing valid Http headers
            server: A watson.common.datastructures.MultiDict containing server variables
            cookies: A watson.http.cookies.CookieDict containing watson.http.cookies.TastyMorsel objects
            body: The content of the request
        """
        super(Request, self).__init__(body=body, headers=headers)
        self._method = str(method).upper()
        if self.method not in REQUEST_METHODS:
            raise TypeError('Not a valid Http Request method.')
        self._get = get or MultiDict()
        self._post = post or MultiDict()
        self._files = files or MultiDict()
        self._server = server or MultiDict()
        self._cookies = cookies or CookieDict()
        self.headers = headers or HeaderDict()

    def __str__(self):
        return '{0} {1} HTTP/{2}\r\n{3}\r\n\r\n{4}'.format(self.method,
                                                           self.url,
                                                           self.version,
                                                           self.headers,
                                                           self.body)

    def __repr__(self):
        return '<{0} method:{1} url:{2}>'.format(get_qualified_name(self),
                                                 self.method,
                                                 self.url)

    # TODO: Add copy method to create non-immutable dicts
    def __copy__(self):
        return Request(self.method,
                       get=copy(self.get),
                       post=copy(self.post),
                       files=copy(self.files),
                       headers=HeaderDict(copy(self.headers)),
                       server=copy(self.server),
                       cookies=CookieDict(copy(self.cookies)),
                       body=copy(self.body))

    # Convenience methods

    def is_xml_http_request(self):
        """
        Determine whether or not a request has originated via an XmlHttpRequest,
        assuming the relevant header has been set by the request.

        Returns:
            Boolean
        """
        return (
            self.headers.get(
                'X-Requested-With',
                '').lower(
        ) == 'xmlhttprequest'
        )

    def is_secure(self):
        """
        Determine whether or not the request was made via Https.

        Returns:
            Boolean
        """
        if 'Https' in self.headers:
            return self.headers['Https'].lower() == 'https'
        return self.url.scheme.lower() == 'https'

    def is_method(self, method):
        """
        Determine whether or not a request was made via a specific method.

        Usage:
            request = ... # request made via GET
            request.is_method('get') # True

        Args:
            string|list|tuple method: the method or list of methods to check

        Returns:
            Boolean
        """
        if isinstance(method, (tuple, list)):
            method = [m.upper() for m in method]
        else:
            method = method.upper()
        return self.method in method

    def host(self):
        """Determine the real host of a request.

        Returns:
            X_FORWARDED_FOR header variable if set, otherwise a watson.http.uri.Url
            hostname attribute.
        """
        return (
            self.url.hostname if 'X-Forwarded-For' not in self.headers else self.headers.get(
    'X-Forwarded-For')
        )


class Response(MessageMixin):

    """Provides a simple and usable interface for dealing with Http Responses.

    See:
        http://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html

    Usage:
        def app(environ, start_response):
            response = Response(200, body='<h1>Hello World!</h1>')
            response.headers.add('Content-Type', 'text/html', charset='utf-8')
            response.cookies.add('something', 'test')
            start_response(*response.start())
            return [response()]
    """
    _status_code = None
    _cookies = None
    _prepared = False

    @property
    def status_code(self):
        """The status code for the Response.
        """
        return self._status_code or 200

    @status_code.setter
    def status_code(self, code):
        """
        Args:
            Code: an int representing the status code for the Response
        """
        self._status_code = code

    @property
    def status_line(self):
        """The formatted status line including the status code and message.
        """
        return (
            '{0} {1}'.format(
    self.status_code,
     STATUS_CODES.get(self.status_code))
        )

    @property
    def cookies(self):
        """Returns the cookies associated with the Response.
        """
        if not self._cookies:
            self._cookies = CookieDict()
        return self._cookies

    @cookies.setter
    def cookies(self, cookies):
        """Sets the cookies associated with the Response.
        """
        if not isinstance(cookies, CookieDict):
            cookies = CookieDict(cookies)
        self._cookies = cookies

    @property
    def encoding(self):
        """Retrieve the encoding for the response from the headers, defaults to
        UTF-8.
        """
        return self.headers.get_option('Content-Type', 'charset', 'utf-8')

    def __init__(self, status_code=None,
                 headers=None, body=None, version='1.1'):
        """
        Args:
            status_code: an int representing the status code for the Response
            headers: A watson.http.headers.HeaderDict object containing valid response headers.
            body: The content for the response
            version: The Http version for the response
        """
        super(Response, self).__init__(headers=headers, body=body)
        self.status_code = status_code
        self._headers = headers or HeaderDict()
        self.version = str(version)

    def start(self):
        """Return the status_line and headers of the response for use in a WSGI
        application.
        """
        self._prepare()
        return self.status_line, self.headers()

    def raw(self):
        """Return the raw encoded output for the response.
        """
        return str(self).encode(self.encoding)

    def __str__(self):
        self._prepare()
        return 'HTTP/{0} {1}\r\n{2}\r\n\r\n{3}'.format(self.version,
                                                       self.status_line,
                                                       self.headers,
                                                       self.body)

    def _prepare(self):
        if not self._prepared:
            self.headers.add(
    'Content-Length',
     self.body.__len__(),
     replace=True)
            for cookie, morsel in self.cookies.items():
                self.headers.add('Set-Cookie', str(morsel))
            self._prepared = True

    def __call__(self):
        return self.body.encode(self.encoding)
