# -*- coding: utf-8 -*-
import re
from watson.di import ContainerAware
from watson.http.messages import Response, Request
from watson.stdlib.imports import get_qualified_name
# add controller to container (string), then retrieve


class BaseController(ContainerAware):
    def execute(self, **kwargs):
        raise NotImplementedError('You must implement execute')

    def get_execute_method_path(self, **kwargs):
        raise NotImplementedError('You must implement get_execute_method_path')


class BaseHttpController(BaseController):
    _request = None
    _response = None

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        if not isinstance(request, Request):
            raise TypeError('Invalid request type, expected watson.http.messages.Request')
        self._request = request

    @property
    def response(self):
        if not self._response:
            self.response = Response()
        return self._response

    @response.setter
    def response(self, response):
        if not isinstance(response, Response):
            raise TypeError('Invalid response type, expected watson.http.messages.Response')
        self._response = response


class ActionController(BaseHttpController):
    def execute(self, **kwargs):
        method = getattr(self, kwargs.get('action') + '_action')
        try:
            result = method(**kwargs)
        except TypeError:
            result = method()
        return result

    def get_execute_method_path(self, **kwargs):
        path = get_qualified_name(self).lower().split('.')
        action = kwargs.get('action', 'index').lower()
        action = re.sub('.-', '_', action)
        path.append(action)
        return path


class RestController(BaseHttpController):
    def execute(self, **kwargs):
        method = getattr(self, self.request.method)
        try:
            result = method(**kwargs)
        except TypeError:
            result = method()
        return result

    def get_execute_method_path(self, **kwargs):
        path = get_qualified_name(self).lower().split('.')
        path.append(self.request.method.lower())
        return path
