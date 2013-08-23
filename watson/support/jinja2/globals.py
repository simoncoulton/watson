# -*- coding: utf-8 -*-
# Global functions for Jinja2 templates
from watson.di import ContainerAware
from jinja2 import contextfunction


class Url(ContainerAware):
    """Convenience method to access the router from within a Jinja2 template.

    Usage:
        url('route_name', keyword=arg)
    """
    def __call__(self, route_name, **kwargs):
        return self.container.get('router').assemble(route_name, **kwargs)


url = Url  # alias to Url


@contextfunction
def get_request(context):
    """Retrieves the request from the controller.

    Usage:
        {{ get_request() }}
    """
    return context['context']['controller'].request


@contextfunction
def get_flash_messages(context):
    """Retrieves the flash messages from the controller.

    Usage:
        {{ get_flash_messages() }}
    """
    return context['context']['controller'].flash_messages
