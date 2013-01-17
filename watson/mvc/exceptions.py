# -*- coding: utf-8 -*-
import linecache
from watson import __version__
from watson.stdlib.imports import get_qualified_name


class ApplicationError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None):
        if status_code:
            self.status_code = status_code
        super(ApplicationError, self).__init__(message)


class NotFoundError(ApplicationError):
    status_code = 404


class InternalServerError(ApplicationError):
    status_code = 500


class ExceptionHandler(object):
    def __init__(self, config=None):
        self.config = config or {}
        # todo implement config for emailing to admin etc
        pass

    def __call__(self, exc_info, params):
        code, message, cause_message, frames, type = self.__process_exception(exc_info)
        model = {
            'code': code,
            'message': message,
            'cause_message': cause_message,
            'version': __version__,
            'frames': frames,
            'type': type,
            'debug': self.config.get('enabled', True)
        }
        model.update(params)
        return model

    def __process_exception(self, exc_info):
        try:
            code = exc_info[1].status_code
        except:
            code = 500
        exc = exc_info[1]
        message = str(exc)
        cause_message = None
        try:
            exc = exc.__cause__
            tb = exc.__traceback__
            cause_message = str(exc)
            type = get_qualified_name(exc)
        except:
            tb = exc_info[2]
            type = get_qualified_name(exc_info[0])
        frames = []
        while tb is not None:
            frame = tb.tb_frame
            line = tb.tb_lineno
            co = frame.f_code
            file = co.co_filename
            function = co.co_name
            linecache.checkcache(file)
            code = linecache.getline(file, line, frame.f_globals)
            frames.append({
                'line': line,
                'file': file,
                'function': function,
                'code': code.strip(),
                'vars': frame.f_locals.items()
            })
            tb = tb.tb_next
        frames.reverse()
        return code, message, cause_message, frames, type
