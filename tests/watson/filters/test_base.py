# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.filters.base import BaseFilter


class TestFilterBase(object):
    @raises(NotImplementedError)
    def test_call_error(self):
        BaseFilter()('value')
