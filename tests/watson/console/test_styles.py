# -*- coding: utf-8 -*-
from watson.console.styles import underline, bold


class TestStyles(object):
    def test_underline(self):
        assert underline('test') == '\033[4mtest\033[0m'
        assert underline('test', terminate=False) == '\033[4mtest'

    def test_bold(self):
        assert bold('test') == '\033[1mtest\033[0m'
        assert bold('test', terminate=False) == '\033[1mtest'
