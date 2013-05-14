# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.validators import base


class TestBaseValidator(object):
    @raises(NotImplementedError)
    def test_call_error(self):
        base.Validator()('value')
