# -*- coding: utf-8 -*-
import cgi
import collections
from urllib.parse import parse_qsl
from watson.common.contextmanagers import ignored
from watson.common.datastructures import MultiDict


__all__ = ['get_form_vars']


def get_form_vars(environ):
    """Convert environ vars into GET/POST/FILES objects.

    Process all get and post vars from a <form> and return MultiDict of
    each.
    """
    if environ['REQUEST_METHOD'] == 'PUT' and not environ.get('CONTENT_TYPE'):
        environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
    field_storage = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ,
                                     keep_blank_values=True)
    get = MultiDict()
    for name, value in parse_qsl(environ.get('QUERY_STRING'),
                                 keep_blank_values=True):
        get[name] = value if value else ''
    return _process_field_storage(field_storage, get=get)


File = collections.namedtuple(
    'File',
    'data filename name type type_options disposition disposition_options headers')


def _process_field_storage(fields, get=None, post=None, files=None):
    if not get:
        get = MultiDict()
    if not post:
        post = MultiDict()
    if not files:
        files = MultiDict()
    with ignored(Exception):
        for name in fields:
            field = fields[name] if isinstance(name, str) else name
            if isinstance(field, list):
                _process_field_storage(field, get, post, files)
            elif field.filename:
                # An uploaded file, create a new File tuple to resolve the
                # not indexable issue.
                files[field.name] = File(
                    field.file,
                    field.filename,
                    field.name,
                    field.type,
                    field.type_options,
                    field.disposition,
                    field.disposition_options,
                    field.headers)
            elif field.disposition or field.name not in get:
                post[field.name] = field.value
            else:
                pass  # pragma: no cover
    return get, post, files
