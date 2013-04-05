# -*- coding: utf-8 -*-
from wsgiref import util


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


def sample_start_response(status, headers):
    pass


def sample_app(environ, start_response):
    return True
