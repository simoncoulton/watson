# -*- coding: utf-8 -*-
from importlib import import_module


def load_definition_from_string(qualified_module):
    """
    Load a definition based on a fully qualified string.

    Usage:
        definition = load_definition_from_string('watson.http.messages.Request')
        request = definition()

    Return:
        None or the loaded object
    """
    parts = qualified_module.split('.')
    try:
        module = import_module('.'.join(parts[:-1]))
        obj = getattr(module, parts[-1:][0])
        return obj
    except ImportError:
        return None


def get_qualified_name(obj):
    """
    Retrieve the full module path of an object.

    Usage:
        from watson.http.messages import Request
        request = Request()
        name = get_qualified_name(request) # watson.http.messages.Request
    """
    try:
        name = obj.__qualname__
    except AttributeError:
        if hasattr(obj, '__name__'):
            name = obj.__name__
        else:
            name = obj.__class__.__name__
    try:
        module = obj.__module__
        return '{0}.{1}'.format(module, name)
    except:
        return name
