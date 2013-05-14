# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.filters import base


class TestFilterBase(object):
    @raises(NotImplementedError)
    def test_call_error(self):
        base.Filter()('value')
