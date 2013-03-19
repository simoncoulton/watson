# -*- coding: utf-8 -*-
from watson.filters.string import Trim, RegEx, Numbers, Upper, Lower


class TestTrim(object):
    def test_trim_string(self):
        filter = Trim()
        assert filter(' Test') == 'Test'
        assert filter('Test') == 'Test'


class TestUpper(object):
    def test_to_upper(self):
        filter = Upper()
        assert filter('test') == 'TEST'


class TestLower(object):
    def test_to_upper(self):
        filter = Lower()
        assert filter('TEST') == 'test'


class TestRegEx(object):
    def test_replace_string(self):
        filter = RegEx('ing', replacement='ed')
        assert filter('testing') == 'tested'


class TestNumbers(object):
    def test_remove_numbers(self):
        filter = Numbers()
        assert filter('ab1234') == '1234'
