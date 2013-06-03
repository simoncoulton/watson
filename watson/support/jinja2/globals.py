# -*- coding: utf-8 -*-
# Global functions for Jinja2 templates
from watson.di import ContainerAware


class Url(ContainerAware):
    """Convenience method to access the router from within a Jinja2 template.

    Usage:
        url('route_name', keyword=arg)
    """
    def __call__(self, route_name, **kwargs):
        return self.container.get('router').assemble(route_name, **kwargs)


url = Url  # alias to Url
