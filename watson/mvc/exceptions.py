# -*- coding: utf-8 -*-


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
