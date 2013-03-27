# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.html.elements import flatten_attributes, TagMixin


class TestFlattenAttributes(object):
    def test_flatten(self):
        attrs = {'class': 'menu', 'id': 'MainMenu'}
        assert flatten_attributes(attrs) == 'class="menu" id="MainMenu"'


class TestTagMixin(object):
    def test_initialize(self):
        mixin = TagMixin(id='Test')
        assert 'id' in mixin.attributes

    @raises(NotImplementedError)
    def test_render(self):
        str(TagMixin(id='Test'))
