# -*- coding: utf-8 -*-
import re
from watson.di import ContainerAware
from watson.events.types import Event
from watson.http.messages import Response, Request
from watson.common.imports import get_qualified_name


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
    _event = None

    @property
    def event(self):
        """The event that was triggered that caused the execution of the
        controller.

        Returns:
            watson.events.types.Event
        """
        return self._event

    @event.setter
    def event(self, event):
        """Set the request object.

        Args:
            watson.events.types.Event event: The triggered event.

        Raises:
            TypeError if the event type is not a subclass of watson.events.types.Event
        """
        if not isinstance(event, Event):
            raise TypeError('Invalid request type, expected watson.events.types.Event')
        self._event = event

    @property
    def request(self):
        """The HTTP request relating to the controller.

        Returns:
            watson.http.messages.Request
        """
        return self._request

    @request.setter
    def request(self, request):
        """Set the request object.

        Args:
            watson.http.messages.Request request: The request associated with the controller.

        Raises:
            TypeError if the request type is not of watson.http.messages.Request
        """
        if not isinstance(request, Request):
            raise TypeError('Invalid request type, expected watson.http.messages.Request')
        self._request = request

    @property
    def response(self):
        """The HTTP response related to the controller.

        If no response object has been set, then a new one will be generated.

        Returns:
            watson.http.messages.Response
        """
        if not self._response:
            self.response = Response()
        return self._response

    @response.setter
    def response(self, response):
        """Set the request object.

        Args:
            watson.http.messages.Response response: The response associated with the controller.

        Raises:
            TypeError if the request type is not of watson.http.messages.Response
        """
        if not isinstance(response, Response):
            raise TypeError('Invalid response type, expected watson.http.messages.Response')
        self._response = response

    def url(self, route_name, params=None):
        """Converts a route into a url.

        Args:
            string route_name: The name of the route to convert
            dict params: The params to use on the route

        Returns:
            The assembled url.
        """
        if not params:
            params = {}
        router = self.container.get('router')
        return router.assemble(route_name, **params)

    def redirect(self, path, params=None, status_code=302, is_url=False, clear=False):
        """Redirect to a different route.

        Redirecting will bypass the rendering of the view, and the body of the
        request will be displayed.

        Also supports Post Redirect Get (http://en.wikipedia.org/wiki/Post/Redirect/Get)
        which can allow post variables to accessed from a GET resource after a
        redirect (to repopulate form fields for example).

        Args:
            string path: The URL or route name to redirect to
            dict params: The params to send to the route
            int status_code: The status code to use for the redirect
            bool is_url: Whether or not the path is a url or route
            bool clear: Whether or not the session data should be cleared

        Returns:
            A watson.http.messages.Response object.
        """
        self.response.status_code = status_code
        if self.request.is_method(('POST', 'PUT')):
            self.response.status_code = status_code if status_code != 302 else 303
            self.request.session['post_redirect_get'] = dict(self.request.post)
        if clear:
            del self.request.session['post_redirect_get']
        url = path if is_url else self.url(path, params)
        self.response.headers.add('location', url, replace=True)
        return self.response

    @property
    def redirect_vars(self):
        post_vars = {}
        if hasattr(self.request, 'session'):
            post_vars = self.request.session.get('post_redirect_get', {})
        return post_vars

    def clear_redirect_vars(self):
        self.request.session['post_redirect_get'] = {}


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
