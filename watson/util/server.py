# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from watson.util.middleware import StaticFileMiddleware
from watson.util.reloader import main


def make_dev_server(app, host='127.0.0.1', port=8000, do_reload=True):
    """
    A simple local development server utilizing the existing simple_server
    module, but allows for serving of static files.

    Never use this in production. EVER.

    Usage:
        def my_app(environ, start_response):
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [b'<h1>Hello World!</h1>']

        if __name__ == '__main__':
            make_dev_server(my_app)

    Args:
        app: A WSGI callable
        host: The host
        port: The port
        do_reload: Whether or not to automatically reload the application when
                   source code changes.
    """
    wrapped_app = StaticFileMiddleware(app)
    if do_reload:
        main(__run_server, (wrapped_app, host, port))
    else:
        try:
            __run_server(wrapped_app, host, port)
        except KeyboardInterrupt:
            print('\nTerminated.')


def __run_server(app, host, port):
    print('Serving application at http://{0}:{1} in your favorite browser...'.format(host, port))
    httpd = make_server(host, port, app)
    httpd.serve_forever()
