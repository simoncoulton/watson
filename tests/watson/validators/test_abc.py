# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.validators import abc


class TestBaseValidator(object):
    @raises(TypeError)
    def test_call_error(self):
        abc.Validator()
