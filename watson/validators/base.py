# -*- coding: utf-8 -*-


class Validator(object):
    """All validators must extend the BaseValidator or be callable.

    Exceptions raised by validators must be of type ValueError.
    """
    message = None

    def __call__(self, value):
        raise NotImplementedError('Validator must be callable.')
