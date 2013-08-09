# -*- coding: utf-8 -*-
import __main__
import os
import mimetypes
import stat


class StaticFileMiddleware(object):

    """
    A WSGI compatibile Middleware class that allows content to be retrieved
    from the directory that the __main__ is called from.

    Usage:
        def app(environ, start_response):
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'Hello World!']

        my_app = StaticFileMiddleware(app)
    """
    app = None
    initial_dir = None
    script_path = None

    def __init__(self, app, initial_dir=None):
        self.script_path = os.path.abspath(__main__.__file__)
        self.initial_dir = initial_dir or os.getcwd()
        self.app = app

    def __call__(self, environ, start_response):
        path = os.path.join(self.initial_dir, environ['PATH_INFO'][1:])
        try:
            return self.serve_static(path,
                                     os.stat(os.path.join(path)),
                                     environ,
                                     start_response)
        except:
            return self.app(environ, start_response)

    def serve_static(self, path, file_stat, environ, start_response):
        if stat.S_ISDIR(file_stat.st_mode):
            raise Exception('Cannot serve a directory')
        if stat.S_ISREG(file_stat.st_mode):
            mime = mimetypes.guess_type(path)[0]
            start_response('200 OK', [
                ('Content-Type', '{0}; charset=utf-8'.format(mime)),
                ('Content-Length', str(os.path.getsize(path)))
            ])
            with open(path, 'rb') as file:
                contents = file.read()
            return [contents]
