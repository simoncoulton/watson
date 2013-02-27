# -*- coding: utf-8 -*-
import collections
from watson.form import fields


class TestFieldMixin(object):
    def test_create_field_mixin(self):
        pass


class TestInputField(object):
    def test_create(self):
        field = fields.Input(name='test', type='blah')
        assert field.value == None
        assert field.name == 'test'
        assert str(field) == '<input name="test" type="blah" />'


class TestTextInputField(object):
    def test_create(self):
        field = fields.Text(name='test')
        assert field.value == None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Text(name='test')
        assert str(field) == '<input name="test" type="text" />'
        field_with_value = fields.Text(name='test', value=1)
        assert str(field_with_value) == '<input name="test" type="text" value="1" />'

    def test_render_with_label(self):
        field = fields.Text(name='test')
        assert field.render_with_label() == '<label for="test">test</label><input name="test" type="text" />'

    # todo filter/validate


class TestTextareaField(object):
    def test_create(self):
        field = fields.Textarea(name='test')
        assert field.value == None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Textarea(name='test')
        assert str(field) == '<textarea name="test"></textarea>'
        field_with_value = fields.Textarea(name='test', value=1)
        assert str(field_with_value) == '<textarea name="test">1</textarea>'

    def test_render_with_label(self):
        field = fields.Textarea(name='test', label='My Test')
        assert field.render_with_label() == '<label for="test">My Test</label><textarea name="test"></textarea>'

    # todo filter/validate


class TestButtonField(object):
    def test_create(self):
        field = fields.Button(name='test')
        assert field.value == None
        assert field.name == 'test'

    def test_render(self):
        field = fields.Button(name='test')
        assert str(field) == '<button name="test">test</button>'
        field_with_value = fields.Button(name='test', value=1)
        assert str(field_with_value) == '<button name="test" value="1">test</button>'

    def test_render_with_label(self):
        field = fields.Button(name='test', label='My Test')
        assert field.render_with_label() == '<button name="test">My Test</button>'

    # todo filter/validate


class TestSelectField(object):
    def test_create(self):
        field = fields.Select(name='test', options=[])
        assert field.value == None
        assert field.name == 'test'

    def test_render_no_options(self):
        field = fields.Select(name='test', options=[])
        assert str(field) == '<select name="test"></select>'

    def test_render_options_list(self):
        field = fields.Select(name='test', options=[1, 2, 3])
        assert str(field) == '<select name="test"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select>'
        field_with_value = fields.Select(name='test', options=[1, 2, 3], value=2)
        assert str(field_with_value) == '<select name="test"><option value="1">1</option><option value="2" selected="selected">2</option><option value="3">3</option></select>'

    def test_render_options_dict(self):
        field = fields.Select(name='test', options={'Test': 'Value'})
        assert str(field) == '<select name="test"><option value="Value">Test</option></select>'

    def test_render_with_label(self):
        field = fields.Select(name='test', label='My Test')
        assert field.render_with_label() == '<label for="test">My Test</label><select name="test"></select>'

    def test_multiple_values(self):
        field = fields.Select(name='test', value=(1, 2), options=[1, 2, 3, 4])
        assert str(field) == '<select multiple="multiple" name="test"><option value="1" selected="selected">1</option><option value="2" selected="selected">2</option><option value="3">3</option><option value="4">4</option></select>'

    def test_optgroup(self):
        field = fields.Select(name='test', options=collections.OrderedDict([('Group One', [1, 2]), ('Group Two', [3, 4])]))
        assert str(field) == '<select name="test"><optgroup label="Group One"><option value="1">1</option><option value="2">2</option></optgroup><optgroup label="Group Two"><option value="3">3</option><option value="4">4</option></optgroup></select>'


    # todo filter/validate
