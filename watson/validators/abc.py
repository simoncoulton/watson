# -*- coding: utf-8 -*-
import abc


class Validator(metaclass=abc.ABCMeta):
    """All validators must extend the BaseValidator or be callable.

    Exceptions raised by validators must be of type ValueError.
    """
    message = None

    @abc.abstractmethod
    def __call__(self, value):
        raise NotImplementedError  # pragma: no cover
