# -*- coding: utf-8 -*-


class BaseValidator(object):
    message = None

    def __call__(self, value):
        raise NotImplementedError('Validator must be callable.')
