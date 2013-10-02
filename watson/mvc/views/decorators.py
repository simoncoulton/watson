# -*- coding: utf-8 -*-
from watson.mvc import views


def view(func=None, template=None, format=None):
    """Return the view model in a specific format and with a specific template.

    This will not work if the response returned from the controller is of
    the watson.http.messages.Response type.

    Args:
        callable func: the function that is being wrapped
        string template: the template to use
        string format: the format to output as

    Returns:
        The view model in the specific format

    Usage:
        class MyClass(controllers.Rest):
            @view(template='edit')
            def create_action(self):
                return 'something'
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            controller_response = func(self, *args, **kwargs)
            if isinstance(controller_response, str):
                controller_response = {'content': controller_response}
            if isinstance(controller_response, dict):
                controller_response = views.Model(data=controller_response)
            if format:
                controller_response.format = format
            if template:
                controller_response.template = template
            return controller_response
        return wrapper
    if func:
        return decorator(func)
    else:
        return decorator
