# -*- coding: utf-8 -*-
from watson.console.styles import format_style


HEADER = '\033[95m'
OK_BLUE = '\033[94m'
OK_GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'


def header(string):
    return format_style(string, HEADER)


def ok_green(string):
    return format_style(string, OK_GREEN)


def ok_blue(string):
    return format_style(string, OK_BLUE)


def warning(string):
    return format_style(string, WARNING)


def fail(string):
    return format_style(string, FAIL)
