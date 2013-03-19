# -*- coding: utf-8 -*-
from watson.validators.base import BaseValidator


class Range(BaseValidator):
    def __init__(self, min=None, max=None, message='"{value}" is not between {min} and {max}'):
        self.message = message
        if not max or not min:
            raise ValueError('Min and max must be specified')
        if min > max:
            raise ValueError('Min cannot be greater than max')
        self.min = min
        self.max = max

    def __call__(self, value):
        valid = True
        if value > self.max or value < self.min:
            raise ValueError(self.message.format(value=value, min=self.min, max=self.max))
        return valid
