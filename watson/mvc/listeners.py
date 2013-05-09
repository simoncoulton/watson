# -*- coding: utf-8 -*-
# TODO: Refactor these into single functions rather than classes where appropriate
import os
import sys
from watson.di import ContainerAware
from watson.http import MIME_TYPES
from watson.http.messages import Response
from watson.mvc.exceptions import NotFoundError, InternalServerError
from watson.mvc.views import Model
from watson.mvc.exceptions import ExceptionHandler
from watson.common.imports import get_qualified_name


class BaseListener(object):
    def __call__(self, event):
        raise NotImplementedError('You must implement __call__')


class RouteListener(BaseListener):
    def __call__(self, event):
        router, request = event.params['router'], event.params['request']
        matches = router.matches(request)
        if not matches:
            raise NotFoundError('Route not found for request: {0}'.format(request.url), 404)
        event.params['route_match'] = matches[0]
        return matches[0]


class DispatchExecuteListener(BaseListener):
    def __init__(self, templates):
        self.templates = templates

    def __call__(self, event):
        route_match = event.params['route_match']
        try:
            controller_class = route_match.params['controller']
            event.params['container'].add(controller_class, controller_class, 'prototype')
            controller = event.params['container'].get(controller_class)
        except Exception as exc:
            raise InternalServerError('Controller not found for route: {0}'.format(route_match.name)) from exc
        event.params['controller_class'] = controller
        controller.event = event
        controller.request = event.params['request']
        try:
            model_data = controller.execute(**route_match.params)
            short_circuit = False
            if isinstance(model_data, str):
                model_data = {'content': model_data}
            elif isinstance(model_data, Response):
                short_circuit = True
                response = model_data
            if not short_circuit:
                controller_path = controller.get_execute_method_path(**route_match.params)
                controller_template = os.path.join(*controller_path)
                response = Model(format=route_match.params.get('format', 'html'),
                                 template=self.templates.get(controller_template, controller_template),
                                 data=model_data)
        except Exception as exc:
            raise InternalServerError('An error occurred executing controller: {0}'.format(get_qualified_name(controller))) from exc
        controller.request.session_to_cookie()
        if controller.request.cookies.modified:
            controller.response.cookies.merge(controller.request.cookies)
        return response


class ExceptionListener(BaseListener):
    def __init__(self, handler, templates):
        self.handler = handler
        self.templates = templates

    def __call__(self, event):
        exception = event.params['exception']
        status_code = exception.status_code
        return Model(format='html',  # should this take the format from the request?
                     template=self.templates.get(str(status_code), self.templates['500']),
                     data=self.handler(sys.exc_info(), event.params))


class RenderListener(BaseListener):
    def __init__(self, view_config):
        self.view_config = view_config

    def __call__(self, event):
        response, view_model = event.params['response'], event.params['view_model']
        renderers = self.view_config['renderers']
        renderer = renderers.get(view_model.format, renderers['default'])
        mime_type = MIME_TYPES[view_model.format][0]
        renderer_instance = event.params['container'].get(renderer['name'])
        try:
            response.body = renderer_instance(view_model)
            response.headers.add('Content-Type', mime_type)
        except Exception as exc:
            raise InternalServerError('Template ({0}) not found'.format(view_model.template)) from exc
