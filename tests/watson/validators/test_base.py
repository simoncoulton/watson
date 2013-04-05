# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.validators.base import BaseValidator


class TestBaseValidator(object):
    @raises(NotImplementedError)
    def test_call_error(self):
        BaseValidator()('value')
