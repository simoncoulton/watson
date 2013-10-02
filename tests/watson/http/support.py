# -*- coding: utf-8 -*-
# Support functions, classes
from wsgiref import util


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


class SampleField(object):
    name = 'test'
    value = 'test'
