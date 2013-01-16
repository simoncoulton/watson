# -*- coding: utf-8 -*-
import os
import traceback
from watson.di import ContainerAware
from watson.http import MIME_TYPES
from watson.mvc.exceptions import NotFoundError, InternalServerError
from watson.mvc.views import Model


class BaseListener(ContainerAware):
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


class DispatchListener(BaseListener):
    def __call__(self, event):
        route_match = event.params['route_match']
        try:
            controller_class = route_match.params['controller']
            self.container.add(controller_class, controller_class, 'prototype')
            controller = self.container.get(controller_class)
        except:
            raise InternalServerError('Controller not found for route: {0}'.format(route_match.name))
        event.params['controller_class'] = controller
        controller.request = event.params['request']
        try:
            model_data = controller.execute(**route_match.params)
            if isinstance(model_data, str):
                model_data = {'content': model_data}
            templates = self.container.get('application.config')['views']['templates']
            controller_template = os.path.join(*controller.get_execute_method_path(**route_match.params)[1:])
            return Model(format=route_match.params.get('format', 'html'),
                         template=templates.get(controller_template, controller_template),
                         data=model_data)
        except:
            raise InternalServerError('An error occurred executing controller {0}'.format(controller.__repr__()))


class ExceptionListener(BaseListener):
    def __call__(self, event):
        # todo flatten exception
        exception = event.params['exception']
        templates = self.container.get('application.config')['views']['templates']
        return Model(format='html',  # should this take the format from the request?
                     template=templates.get(str(exception.status_code), templates['500']),
                     data={'code': exception.status_code, 'message': str(exception), 'stack': traceback.format_exc()})


class RenderListener(BaseListener):
    def __call__(self, event):
        response, view_model = event.params['response'], event.params['view_model']
        view_config = self.container.get('application.config')['views']
        renderers = view_config['renderers']
        renderer = renderers.get(view_model.format, renderers['default'])
        mime_type = MIME_TYPES[view_model.format][0]
        renderer_instance = self.container.get(renderer['name'])
        response.headers.add('Content-Type', mime_type)
        response.body = renderer_instance(view_model)
