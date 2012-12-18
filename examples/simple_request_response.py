# -*- coding: utf-8 -*-
# Runs an extremely simple web application on the development server
# and auto-reloads on change.
import os
import sys
from wsgiref.util import setup_testing_defaults

sys.path.append(os.path.abspath('..'))
from watson.http.messages import Response, create_request_from_environ
from watson.util.server import make_dev_server


def simple_request_response(environ, start_response):
    setup_testing_defaults(environ)

    request = create_request_from_environ(environ)
    response = Response(200, body='Hello World!')

    start_response(*response.start())
    return [response()]


if __name__ == '__main__':
    make_dev_server(simple_request_response, do_reload=True)
