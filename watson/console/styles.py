# -*- coding: utf-8 -*-


def underline(string):
    return format_style(string, '\033[4m')


def bold(string):
    return format_style(string, '\033[1m')


def format_style(string, start, end='\033[0m'):
    return '{0}{1}{2}'.format(start, string, end)
