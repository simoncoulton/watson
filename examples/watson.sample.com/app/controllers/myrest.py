# -*- coding: utf-8 -*-
from watson import __version__
from watson.mvc.controllers import RestController


class MyRest(RestController):
    def GET(self):
        return '<h1>Welcome to Watson v{0}!</h1>'.format(__version__)
