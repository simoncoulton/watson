# -*- coding: utf-8 -*-


class BaseFilter(object):
    """All filters must extend the BaseFilter or be callable.
    """
    def __call__(self, value):
        raise NotImplementedError('Filter must be callable.')
