# -*- coding: utf-8 -*-
from cgi import FieldStorage
from urllib.parse import parse_qsl
from watson.stdlib.datastructures import MultiDict


def get_form_vars(environ):
    """
    Process all get and post vars from a <form> and return MultiDict of
    each.
    """
    keep_blank_values = True
    if environ['REQUEST_METHOD'] == 'PUT' and not environ.get('CONTENT_TYPE'):
        environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
    field_storage = FieldStorage(fp=environ['wsgi.input'], environ=environ,
                                 keep_blank_values=keep_blank_values)
    get = MultiDict()
    for name, value in parse_qsl(environ.get('QUERY_STRING')):
        get[name] = value
    return _process_field_storage(field_storage, get=get)


def _process_field_storage(fields, get=None, post=None, files=None):
    if not get:
        get = MultiDict()
    if not post:
        post = MultiDict()
    if not files:
        files = MultiDict()
    try:
        for name in fields:
            field = fields[name] if isinstance(name, str) else name
            if isinstance(field, list):
                _process_field_storage(field, get, post, files)
            elif field.filename:
                files[field.name] = field
            elif field.disposition or field.name not in get:
                post[field.name] = field.value
            else:
                if field.name not in get:
                    get[field.name] = field.value
    except:
        pass
    return get, post, files
