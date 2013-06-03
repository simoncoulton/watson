# -*- coding: utf-8 -*-
# Filter functions for Jinja2 templates
from watson.common import imports


def get_qualified_name(obj):
    return imports.get_qualified_name(obj)
