# -*- coding: utf-8 -*-
from watson.console.colors import header, ok_blue, ok_green, warning, fail


class TestColors(object):

    def test_header(self):
        assert header('test') == '\033[95mtest\033[0m'
        assert header('test', terminate=False) == '\033[95mtest'

    def test_ok_green(self):
        assert ok_green('test') == '\033[92mtest\033[0m'
        assert ok_green('test', terminate=False) == '\033[92mtest'

    def test_ok_blue(self):
        assert ok_blue('test') == '\033[94mtest\033[0m'
        assert ok_blue('test', terminate=False) == '\033[94mtest'

    def test_warning(self):
        assert warning('test') == '\033[93mtest\033[0m'
        assert warning('test', terminate=False) == '\033[93mtest'

    def test_fail(self):
        assert fail('test') == '\033[91mtest\033[0m'
        assert fail('test', terminate=False) == '\033[91mtest'
