# -*- coding: utf-8 -*-
import collections


class TagMixin(object):

    """Simple tag mixin used for all html tags.

    All keyword arguments that get passed to __init__ will be converted into
    attributes for the element.

    Attributes:
        dict attributes: a dictionary of attributes associated with the tag.
    """
    attributes = None

    def __init__(self, **kwargs):
        self.attributes = collections.ChainMap(kwargs)

    def __str__(self):
        return self.render()

    def render(self):
        raise NotImplementedError('The render method has not been implemented')


def flatten_attributes(attrs, keep_empty=False):
    """Flattens attributes into a single string of key=value pairs.

    Attributes are sorted alphabetically.
    """
    value_check = lambda val: True if keep_empty else True if val else False
    return ' '.join(['{0}="{1}"'.format(name, value or '') for name, value
                    in sorted(attrs.items()) if value_check(value)])
