# -*- coding: utf-8 -*-
from functools import update_wrapper


def cached_property(func):
    prop = '_{name}'.format(name=func.__name__)

    def _get_property(self):
        try:
            value = getattr(self, prop)
        except AttributeError:
            value = func(self)
            setattr(self, prop, value)
        return value

    update_wrapper(_get_property, func)

    def _del_property(self):
        delattr(self, prop)

    return property(_get_property, None, _del_property)
