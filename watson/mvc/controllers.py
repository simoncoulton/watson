# -*- coding: utf-8 -*-
import re
from watson.di import ContainerAware
from watson.http.messages import Response, Request
from watson.stdlib.imports import get_qualified_name


class BaseController(ContainerAware):
    """
    The interface for controller classes.
    """
    def execute(self, **kwargs):
        raise NotImplementedError('You must implement execute')

    def get_execute_method_path(self, **kwargs):
        raise NotImplementedError('You must implement get_execute_method_path')

    def __repr__(self):
        return '<{0}>'.format(get_qualified_name(self))


class HttpControllerMixin(BaseController):
    """
    A mixin for controllers that can contain http request and response objects.

    Attributes:
        _request: The request made that has triggered the controller
        _response: The response that will be returned by the controller
    """
    _request = None
    _response = None

    @property
    def request(self):
        """
        Returns:
            watson.http.messages.Request
        """
        return self._request

    @request.setter
    def request(self, request):
        """
        Set the request object.

        Raises:
            TypeError if the request type is not of watson.http.messages.Request
        """
        if not isinstance(request, Request):
            raise TypeError('Invalid request type, expected watson.http.messages.Request')
        self._request = request

    @property
    def response(self):
        """
        If no response object has been set, then a new one will be generated.

        Returns:
            watson.http.messages.Response
        """
        if not self._response:
            self.response = Response()
        return self._response

    @response.setter
    def response(self, response):
        """
        Set the request object.

        Raises:
            TypeError if the request type is not of watson.http.messages.Response
        """
        if not isinstance(response, Response):
            raise TypeError('Invalid response type, expected watson.http.messages.Response')
        self._response = response

    # todo redirect


class ActionController(HttpControllerMixin):
    """
    Usage:
        class MyController(ActionController):
            def my_func_action(self):
                return 'something'
    """
    def execute(self, **kwargs):
        method = getattr(self, kwargs.get('action', 'index') + '_action')
        try:
            result = method(**kwargs)
        except TypeError:
            result = method()
        return result

    def get_execute_method_path(self, **kwargs):
        return [self.__class__.__name__.lower(),
                re.sub('.-', '_', kwargs.get('action', 'index').lower())]


class RestController(HttpControllerMixin):
    """
    Usage:
        class MyController(RestController):
            def GET(self):
                return 'something'
    """
    def execute(self, **kwargs):
        method = getattr(self, self.request.method)
        try:
            result = method(**kwargs)
        except TypeError:
            result = method()
        return result

    def get_execute_method_path(self, **kwargs):
        return [self.__class__.__name__.lower(), self.request.method.lower()]
