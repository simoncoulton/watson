# -*- coding: utf-8 -*-
TERMINATE = '\033[0m'


def underline(string, terminate=True):
    return format_style(string, '\033[4m', TERMINATE if terminate else '')


def bold(string, terminate=True):
    return format_style(string, '\033[1m', TERMINATE if terminate else '')


def format_style(string, start, end=TERMINATE):
    return '{0}{1}{2}'.format(start, string, end)
