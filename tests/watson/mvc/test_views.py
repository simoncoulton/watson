# -*- coding: utf-8 -*-
from watson.mvc.views import XmlRenderer, JsonRenderer
from tests.watson.mvc.support import sample_view_model


class TestXmlRenderer(object):
    def test_output(self):
        renderer = XmlRenderer()
        output = renderer(sample_view_model())
        assert output == '<?xml version="1.0" encoding="utf-8" ?><test><nodes><node>Testing</node><node>Another node</node></nodes></test>'


class TestJsonRenderer(object):
    def test_output(self):
        renderer = JsonRenderer()
        output = renderer(sample_view_model())
        assert output == '{"test": {"nodes": {"node": ["Testing", "Another node"]}}}'
