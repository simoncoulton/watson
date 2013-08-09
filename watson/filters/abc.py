# -*- coding: utf-8 -*-
import abc


class Filter(metaclass=abc.ABCMeta):

    """All filters must extend the BaseFilter or be callable.
    """
    @abc.abstractmethod
    def __call__(self, value):
        raise NotImplementedError  # pragma: no cover
