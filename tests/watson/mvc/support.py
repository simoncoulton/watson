# -*- coding: utf-8 -*-
# Support functions, classes
from wsgiref import util
from watson.mvc.controllers import ActionController, RestController
from watson.mvc.views import Model


def start_response(status_line, headers):
    pass


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


class SampleActionController(ActionController):
    def something_action(self, **kwargs):
        return 'something_action'

    def blah_action(self):
        return 'blah_action'


class SampleRestController(RestController):
    def GET(self):
        return 'GET'


def sample_view_model():
    return Model(format='html', template=None, data={"test": {"nodes": {"node": ["Testing", "Another node"]}}})
