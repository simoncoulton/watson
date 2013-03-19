# -*- coding: utf-8 -*-
import re
from watson.validators.base import BaseValidator


class Length(BaseValidator):
    def __init__(self, min=-1, max=-1, message='"{value}" does not meet the required length of {length}'):
        self.message = message
        if max > -1 and min > max:
            raise ValueError('Min cannot be greater than max')
        if min > -1 and max > -1 and max < min:
            raise ValueError('Max cannot be greater than min')
        self.min = int(min)
        self.max = int(max)

    def __call__(self, value):
        str_len = len(value)
        valid = True
        message = None
        if (self.min > -1 and str_len < self.min) or (self.max > -1 and str_len > self.max):
            valid = False
            message = self.message.format(min=self.min, max=self.max, value=value, length=str_len)
        if not valid:
            raise ValueError(message)
        return valid


class Required(BaseValidator):
    def __init__(self, message='Value is required'):
        self.message = message

    def __call__(self, value):
        if not value:
            raise ValueError(self.message.format(value=value))
        return True


class RegEx(BaseValidator):
    def __init__(self, regex, flags=0, message='"{value}" does not match pattern "{pattern}"'):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, value):
        if not self.regex.match(value):
            raise ValueError(self.message.format(value=value, pattern=self.regex.pattern))
