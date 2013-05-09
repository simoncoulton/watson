# -*- coding: utf-8 -*-
import re
from watson.validators.base import BaseValidator


class Length(BaseValidator):
    """Validates the length of a string.

    Usage:
        validator = Length(1, 10)
        validator('Test')  # True
        validator('Testing maximum')  # raises ValueError
    """
    def __init__(self, min=-1, max=-1, message='"{value}" does not meet the required length'):
        """Initializes the validator.

        Min, max, length are interpolated into the message.

        Args:
            int min: The minimum length of the string.
            int max: The maximum length of the string.
            string message: The message to be used if the validator fails.
        """
        self.message = message
        if max > -1 and min > max:
            raise ValueError('Min cannot be greater than max')
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
    """Validates whether or not a value exists.

    Usage:
        validator = Required()
        validator('Test')  # True
        validator('')  # raises ValueError
    """
    def __init__(self, message='Value is required'):
        self.message = message

    def __call__(self, value):
        if not value:
            raise ValueError(self.message.format(value=value))
        return True


class RegEx(BaseValidator):
    """Validates a value based on a regular expression.

    Usage:
        validator = RegEx('Match')
        validator('Match')  # True
        validator('Other')  # raises ValueError
    """
    def __init__(self, regex, flags=0, message='"{value}" does not match pattern "{pattern}"'):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, value):
        if not self.regex.match(value):
            raise ValueError(self.message.format(value=value, pattern=self.regex.pattern))


class Csrf(BaseValidator):
    """Validates a csrf token.

    Usage:
        validator = Csrf()
        validator('submitted token')
    """
    def __init__(self, token=None, message='Cross-Site request forgery attempt detected, invalid token specified "{token}"'):
        self.token = token
        self.message = message

    def __call__(self, value):
        if value != self.token:
            raise ValueError(self.message.format(token=value))
