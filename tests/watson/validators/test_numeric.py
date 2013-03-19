# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.validators.numeric import Range


class TestRange(object):
    @raises(ValueError)
    def test_does_not_meet_range(self):
        validator = Range(1, 10)
        validator(11)

    def test_does_meet_range(self):
        validator = Range(1, 10)
        validator(5)
        validator(5.4)
        validator('6')

    @raises(ValueError)
    def test_no_min_or_max(self):
        Range()

    @raises(ValueError)
    def test_min_greater_max(self):
        Range(5, 1)
