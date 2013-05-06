# -*- coding: utf-8 -*-
from watson.console.styles import format_style, TERMINATE


HEADER = '\033[95m'
OK_BLUE = '\033[94m'
OK_GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'


def header(string, terminate=True):
    return format_style(string, HEADER, TERMINATE if terminate else '')


def ok_green(string, terminate=True):
    return format_style(string, OK_GREEN, TERMINATE if terminate else '')


def ok_blue(string, terminate=True):
    return format_style(string, OK_BLUE, TERMINATE if terminate else '')


def warning(string, terminate=True):
    return format_style(string, WARNING, TERMINATE if terminate else '')


def fail(string, terminate=True):
    return format_style(string, FAIL, TERMINATE if terminate else '')
