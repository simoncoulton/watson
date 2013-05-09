# -*- coding: utf-8 -*-
from watson.console.styles import format_style, TERMINATE


HEADER = '\033[95m'
OK_BLUE = '\033[94m'
OK_GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'


def header(string, terminate=True):
    """Wraps a string in the terminal colors for headers.

    Usage:
        header('some text')  # colored text in terminal

    Args:
        string string: The string to wrap
        boolean terminate: Whether or not to terminate the color
    """
    return format_style(string, HEADER, TERMINATE if terminate else '')


def ok_green(string, terminate=True):
    """Wraps a string in the terminal colors for ok green.

    Usage:
        ok_green('some text')  # colored text in terminal

    Args:
        string string: The string to wrap
        boolean terminate: Whether or not to terminate the color
    """
    return format_style(string, OK_GREEN, TERMINATE if terminate else '')


def ok_blue(string, terminate=True):
    """Wraps a string in the terminal colors for ok blue.

    Usage:
        ok_blue('some text')  # colored text in terminal

    Args:
        string string: The string to wrap
        boolean terminate: Whether or not to terminate the color
    """
    return format_style(string, OK_BLUE, TERMINATE if terminate else '')


def warning(string, terminate=True):
    """Wraps a string in the terminal colors for warning.

    Usage:
        warning('some text')  # colored text in terminal

    Args:
        string string: The string to wrap
        boolean terminate: Whether or not to terminate the color
    """
    return format_style(string, WARNING, TERMINATE if terminate else '')


def fail(string, terminate=True):
    """Wraps a string in the terminal colors for fail.

    Usage:
        fail('some text')  # colored text in terminal

    Args:
        string string: The string to wrap
        boolean terminate: Whether or not to terminate the color
    """
    return format_style(string, FAIL, TERMINATE if terminate else '')
