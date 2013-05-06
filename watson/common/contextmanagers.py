# -*- coding: utf-8 -*-
from contextlib import contextmanager


@contextmanager
def ignored(*exceptions):
    """Provides the ability to not have to write try/catch blocks when just
    passing on the except.

    Thanks to Raymond Hettinger from "Transforming Code into Beautiful Idiotmatic Python"
    This will be included in the standard library in 3.4.

    Usage:
        # instead of...
        try:
            do_something()
        except:
            pass

        # use this:
        with ignored(Exception):
            do_something()

    """
    try:
        yield
    except exceptions:
        pass
