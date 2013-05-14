# -*- coding: utf-8 -*-
from watson.common.datastructures import MultiDict
from watson.http.cookies import CookieDict


class HeaderDict(MultiDict):
    """A dictionary of headers and their values.

    Contains a collection of key/value pairs that define a set of headers
    for either a http request or response (e.g. HTTP_ACCEPT)
    """
    def add(self, field, value, replace=False, **options):
        """
        Adds a header to the collection.

        Usage:
            # Content-Type: text/html; charset=utf-8
            headers = HeaderCollection()
            headers.add('Content-Type', 'text/html', charset='utf-8')

        Args:
            field: the field name of the header
            value: the value for the header
            options: any other keyword args to add to the value
        """
        vals = [str(value)]
        if options:
            vals.extend(['{0}={1}'.format(key, val) for
                        key, val in options.items()])
        self.set(parse_from_environ_header_field(field), '; '.join(vals), replace)

    def get_option(self, field, option, default=None):
        """Retrieve an individual option from a header.

        Usage:
            # Content-Type: text/html; charset=utf-8
            headers = HeaderCollection()
            headers.add('Content-Type', 'text/html', charset='utf-8')
            option = headers.get_option('Content-Type', 'charset') # utf-8


        Args:
            field: the header field
            option: the option to retrieve from the field
            default: the default value if the option does not exist

        Returns:
            The default value or the value from the option
        """
        real_field = parse_from_environ_header_field(field)
        if real_field not in self:
            return default
        options = self[real_field].split('; ')
        found = [opt.split('=')[1] for opt in options if opt.split('=')[0] == option]
        return found[0] if found else default

    def __getitem__(self, field):
        return dict.__getitem__(self, parse_from_environ_header_field(field))

    def get(self, field, default=None):
        real_field = parse_from_environ_header_field(field)
        return self[real_field] if real_field in self else default

    def __delitem__(self, field):
        if field in self:
            super(HeaderDict, self).__delitem__(field)

    def __call__(self):
        """Output in a format suitable for a wsgi callable.

        Outputs the header collection as a list of tuple pairs for use in a
        wsgi application.

        Returns:
            A list of tuple pairs
        """
        tuple_pairs = []
        for field, value in sorted(self.items()):
            if (isinstance(value, list)):
                for multi_val in value:
                    tuple_pairs.append((field, multi_val))
            else:
                tuple_pairs.append((field, value))
        return tuple_pairs

    def __str__(self):
        return '\r\n'.join(['{0}: {1}'.format(field, value) for field, value in self()])


def is_header(field):
    """Determine if a field is an acceptable http header.
    """
    return field[:5] == 'HTTP_' or field in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HTTPS')


def http_header(field):
    """Return the correct header field name.
    """
    return field if field[:5] != 'HTTP_' else field[5:]


def parse_to_environ_header_field(field):
    """Converts a http header field into an uppercase form.
    """
    return field.replace('-', '_').upper()


def parse_from_environ_header_field(field):
    """Converts a http header field into a lowercase form.
    """
    return http_header(field).replace('_', ' ').title().replace(' ', '-')


def split_headers_server_vars(environ):
    """Splits the environ into headers and server pairs.
    """
    headers = HeaderDict()
    server = MultiDict()
    cookies = CookieDict()
    for key in environ:
        if is_header(key):
            headers.add(http_header(key), environ[key])
            if key == 'HTTP_COOKIE':
                cookies = CookieDict(environ[key])
                cookies.modified = False
        else:
            server[key] = environ[key]
    return headers, server, cookies
