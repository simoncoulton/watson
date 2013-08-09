# -*- coding: utf-8 -*-
from watson.validators import abc


class Range(abc.Validator):

    """Validates the length of a string.

    Usage:
        validator = Length(1, 10)
        validator('Test')  # True
        validator('Testing maximum')  # raises ValueError
    """

    def __init__(self, min=None, max=None,
                 message='"{value}" is not between {min} and {max}'):
        self.message = message
        if not max or not min:
            raise ValueError('Min and max must be specified')
        if min > max:
            raise ValueError('Min cannot be greater than max')
        self.min = min
        self.max = max

    def __call__(self, value):
        if float(value) > self.max or float(value) < self.min:
            raise ValueError(
                self.message.format(
                    value=value,
                    min=self.min,
                    max=self.max))
        return True
