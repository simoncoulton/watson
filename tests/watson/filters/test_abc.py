# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.filters import abc


class TestFilterBase(object):

    @raises(TypeError)
    def test_call_error(self):
        abc.Filter()
