# -*- coding: utf-8 -*-
import re
from html import _escape_map_full
from html.entities import codepoint2name

html_entities = {_ord: '&{0};'.format(value)
                 for _ord, value in codepoint2name.items()}
html_entities.update(_escape_map_full)
entities_html = {value: _ord for _ord, value in html_entities.items()}


def encode(string):
    """Encodes html entities.

    This is a little more full featured than html.escape, as it will
    replace all charactes from codepoint2name.

    Returns:
        string with replaced html entities.
    """
    return string.translate(html_entities)


def decode(string):
    """Decodes html entities.

    Returns:
        string with html entities decoded.
    """
    return (
        re.sub(
            '&(?:[#a-z][a-z0-9]+);',
            lambda m: chr(entities_html[m.group()]),
            string)
    )
