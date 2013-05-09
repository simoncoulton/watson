# -*- coding: utf-8 -*-

from watson.common.contextmanagers import ignored


def test_ignored_exception():
    with ignored(Exception):
        raise Exception
    assert True
