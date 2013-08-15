# -*- coding: utf-8 -*-
# TODO: Refactor these into single functions rather than classes where
# appropriate
import abc
import os
import sys
from watson.common.imports import get_qualified_name
from watson.di import ContainerAware
from watson.http import MIME_TYPES
from watson.http.messages import Response
from watson.mvc.exceptions import NotFoundError, InternalServerError, ExceptionHandler
from watson.mvc.views import Model


class Base(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __call__(self, event):
        # pragma: no cover
        raise NotImplementedError('You must implement __call__')


class Route(Base):

    def __call__(self, event):
        router, request = event.params['router'], event.params['request']
        matches = router.matches(request)
        if not matches:
            raise NotFoundError(
                'Route not found for request: {0}'.format(request.url),
                404)
        event.params['route_match'] = matches[0]
        return matches[0]


class DispatchExecute(Base):

    def __init__(self, templates):
        self.templates = templates

    def __call__(self, event):
        route_match = event.params['route_match']
        try:
            controller_class = route_match.route.options['controller']
            container = event.params['container']
            if controller_class not in container.config['definitions']:
                container.add(controller_class, controller_class, 'prototype')
            else:
                controller_definition = container.config[
                    'definitions'][controller_class]
                controller_definition['type'] = 'prototype'
                if 'item' not in controller_definition:
                    controller_definition['item'] = controller_class

            controller = event.params['container'].get(controller_class)
        except Exception as exc:
            raise InternalServerError(
                'Controller not found for route: {0}'.format(
                    route_match.route.name)) from exc
        event.params['controller_class'] = controller
        controller.event = event
        controller.request = event.params['request']
        try:
            execute_params = route_match.params
            model_data = controller.execute(**execute_params)
            short_circuit = False
            if isinstance(model_data, str):
                model_data = {'content': model_data}
            elif isinstance(model_data, Response):
                short_circuit = True
                response = model_data
            if not short_circuit:
                controller_path = controller.get_execute_method_path(
                    **route_match.params)
                controller_template = os.path.join(*controller_path)
                view_template = self.templates.get(controller_template,
                                                   controller_template)
                format = route_match.params.get('format', 'html')
                if isinstance(model_data, Model):
                    if not model_data.template:
                        model_data.template = view_template
                    if not model_data.format:
                        model_data.format = format
                    response = model_data
                else:
                    response = Model(
                        format=format,
                        template=view_template,
                        data=model_data)
        except Exception as exc:
            raise InternalServerError(
                'An error occurred executing controller: {0}'.format(get_qualified_name(controller))) from exc
        controller.request.session_to_cookie()
        if controller.request.cookies.modified:
            controller.response.cookies.merge(controller.request.cookies)
        return response


class Exception_(Base):

    def __init__(self, handler, templates):
        self.handler = handler
        self.templates = templates

    def __call__(self, event):
        exception = event.params['exception']
        status_code = exception.status_code
        return Model(format='html',  # should this take the format from the request?
                     template=self.templates.get(
                         str(status_code),
                         self.templates['500']),
                     data=self.handler(sys.exc_info(), event.params))


class Render(Base):

    def __init__(self, view_config):
        self.view_config = view_config

    def __call__(self, event):
        response, view_model = event.params[
            'response'], event.params['view_model']
        renderers = self.view_config['renderers']
        renderer = renderers.get(view_model.format, renderers['default'])
        mime_type = MIME_TYPES[view_model.format][0]
        renderer_instance = event.params['container'].get(renderer['name'])
        try:
            response.body = renderer_instance(view_model)
            response.headers.add('Content-Type', mime_type)
        except Exception as exc:
            raise InternalServerError(
                'Template ({0}) not found'.format(
                    view_model.template)) from exc
