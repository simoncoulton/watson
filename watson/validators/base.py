# -*- coding: utf-8 -*-


class BaseValidator(object):
    """All validators must extend the BaseValidator or be callable.
    """
    message = None

    def __call__(self, value):
        raise NotImplementedError('Validator must be callable.')
