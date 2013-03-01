# -*- coding: utf-8 -*-
from watson.stdlib.imports import get_qualified_name
# todo: csrf field


class TagMixin(object):
    attributes = None

    def __init__(self, **kwargs):
        self.attributes = {}
        self.attributes.update(kwargs)

    def render(self):
        raise NotImplementedError('The render method has not been implemented')


class Label(TagMixin):
    html = '<label for="{0}">{1}</label>'
    text = None

    def __init__(self, text):
        self.text = text

    def render(self, field):
        if not 'id' in field.attributes:
            # inject id based on field name
            field.attributes['id'] = field.name
        return self.html.format(field.attributes['id'], self.text)


class FieldMixin(TagMixin):
    label = None
    html = '{0}'
    validators = None
    filters = None
    _value = None

    def __init__(self, name, value=None, label=None, **kwargs):
        self.label = Label(label or name)
        kwargs['name'] = name
        self.value = value
        super(FieldMixin, self).__init__(**kwargs)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def name(self):
        return self.attributes['name']

    def render_with_label(self):
        raise NotImplementedError('The render method has not been implemented')

    def __str__(self):
        return self.render()

    def __repr__(self):
        return '<{0} name:{1}>'.format(get_qualified_name(self), self.name)


class Input(FieldMixin):
    html = '<input {0} />'

    def render(self):
        attributes = self.attributes.copy()
        if self.value:
            attributes['value'] = str(self.value)

        return self.html.format(flatten_attributes(attributes))

    def render_with_label(self):
        return ''.join((self.label.render(self), self.render()))


class GroupInputMixin(Input):
    label_position = 'left'
    wrapped = True
    values = None
    fieldset_html = '<fieldset><legend>{0}</legend>{1}</fieldset>'

    def __init__(self, name, values=None, value=None, **kwargs):
        super(GroupInputMixin, self).__init__(name, value, **kwargs)
        try:
            iter(values)
            self.values = values
        except:
            self.values = [(self.label.text, values)]

    def has_multiple_elements(self):
        return isinstance(self.values, (tuple, list)) and len(self.values) > 1

    def render(self):
        multiple_elements = self.has_multiple_elements()
        name = '{0}[]'.format(self.name) if multiple_elements else self.name
        elements = []
        for index, label_value_pair in enumerate(self.values):
            attributes = self.attributes.copy()
            label_text, value = label_value_pair
            if multiple_elements:
                element_id = '{0}_{1}'.format(self.name, index)
            else:
                element_id = self.name
            attributes.update({
                'name': name,
                'id': element_id
            })
            if value:
                attributes['value'] = value
            if self.value and value == self.value:
                attributes['checked'] = 'checked'
            flat_attributes = flatten_attributes(attributes)
            element = self.__render_input(element_id, flat_attributes, label_text)
            elements.append(element)
        return ''.join(elements)

    def render_with_label(self):
        multiple_elements = self.has_multiple_elements()
        if multiple_elements:
            wrap_html = self.fieldset_html
        else:
            wrap_html = '{1}'
        return wrap_html.format(self.label.text, self.render())

    def __render_input(self, id, attributes, label_text):
        element = self.html.format(attributes)
        output = '{0}{1}'
        if self.wrapped:
            if self.label_position == 'left':
                return self.label.html.format(id, output.format(label_text, element))
            return self.label.html.format(id, output.format(element, label_text))
        else:
            label = self.label.html.format(id, label_text)
            if self.label_position == 'left':
                return output.format(label, element)
            return output.format(element, label)


class Radio(GroupInputMixin):
    def __init__(self, name, values=None, value=None, **kwargs):
        super(Radio, self).__init__(name, values, value, type='radio', **kwargs)


class Checkbox(GroupInputMixin):
    def __init__(self, name, values=None, value=None, **kwargs):
        super(Checkbox, self).__init__(name, values, value, type='checkbox', **kwargs)


class Button(Input):
    html = '<button {0}>{1}</button>'

    def render(self):
        attributes = self.attributes.copy()
        if self.value:
            attributes['value'] = str(self.value)
        return self.html.format(flatten_attributes(attributes), self.label.text)

    def render_with_label(self):
        return self.render()


class Submit(Input):
    button_mode = False

    def __init__(self, name, value=None, button_mode=False, **kwargs):
        real_value = value or kwargs.get('label', name)
        if button_mode:
            self.html = '<button {0}>{1}</button>'
            self.button_mode = True
        super(Submit, self).__init__(name, real_value, type='submit', **kwargs)

    def render(self):
        if self.button_mode:
            attributes = self.attributes.copy()
            return self.html.format(flatten_attributes(attributes), self.label.text)
        return super(Submit, self).render()

    def render_with_label(self):
        return self.render()


class Textarea(Input):
    html = '<textarea {0}>{1}</textarea>'

    def render(self):
        attributes = self.attributes.copy()
        value = self.value if self.value else ''
        return self.html.format(flatten_attributes(attributes), value)


class Select(FieldMixin):
    html = '<select {0}>{1}</select>'
    option_html = '<option value="{0}"{2}>{1}</option>'
    optgroup_html = '<optgroup label="{0}">{1}</optgroup>'
    options = None

    def __init__(self, name, multiple=False, options=None, value=None, **kwargs):
        self.options = options or []
        if multiple or isinstance(value, (tuple, list)):
            kwargs['multiple'] = 'multiple'
        super(Select, self).__init__(name, value, **kwargs)

    def render(self):
        attributes = self.attributes.copy()
        return self.html.format(flatten_attributes(attributes), self._options_render())

    def render_with_label(self):
        return ''.join((self.label.render(self), self.render()))

    def _options_render(self):
        if isinstance(self.options, dict):
            options = []
            for label, value in self.options.items():
                if isinstance(value, (tuple, list)):
                    options.append(self.optgroup_html.format(label, self.__render_options(value)))
                else:
                    options.append(self.__render_option(label, value))
            return ''.join(options)
        else:
            return self.__render_options(self.options)

    def __render_options(self, options):
        return ''.join([self.__render_option(value, value) for value in options])

    def __render_option(self, label, value):
        match = False
        if value == self.value or (isinstance(self.value, (tuple, list)) and value in self.value):
            match = True
        selected = ' selected="selected"' if match else ''
        return self.option_html.format(value, label, selected)

# Convenience classes for input types


class Text(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Text, self).__init__(name, value, type='text', **kwargs)


class Date(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Date, self).__init__(name, value, type='date', **kwargs)


class Email(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Email, self).__init__(name, value, type='email', **kwargs)


class Hidden(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Hidden, self).__init__(name, value, type='hidden', **kwargs)


class Password(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Password, self).__init__(name, value, type='password', **kwargs)


class File(Input):
    def __init__(self, name, value=None, **kwargs):
        super(File, self).__init__(name, value, type='file', **kwargs)


def flatten_attributes(attrs):
    return ' '.join(['{0}="{1}"'.format(name, value) for name, value in sorted(attrs.items())])
