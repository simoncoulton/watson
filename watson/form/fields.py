# -*- coding: utf-8 -*-


class TagMixin(object):
    attributes = None

    def __init__(self, **kwargs):
        self.attributes = {}
        self.attributes.update(kwargs)


class Label(TagMixin):
    html = '<label for="{0}">{1}</label>'
    text = None

    def __init__(self, text):
        self.text = text

    def render(self, field):
        return self.html.format(field.name, self.text)


class FieldMixin(TagMixin):
    label = None
    html = '{0}'
    _value = None

    def __init__(self, name, value=None, **kwargs):
        self.label = Label(kwargs.get('label', name))
        if 'label' in kwargs:
            del kwargs['label']
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

    def render(self):
        raise NotImplementedError('The render method has not been implemented')

    def render_with_label(self):
        raise NotImplementedError('The render method has not been implemented')

    def __str__(self):
        return self.render()


class Input(FieldMixin):
    html = '<input {0} />'

    def render(self):
        attributes = self.attributes.copy()
        if self.value:
            attributes['value'] = str(self.value)

        return self.html.format(flatten_attributes(attributes))

    def render_with_label(self):
        return ''.join((self.label.render(self), self.render()))


class Radio(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Radio, self).__init__(name, value, type='radio', **kwargs)


class Checkbox(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Checkbox, self).__init__(name, value, type='checkbox', **kwargs)


class Button(Input):
    html = '<button {0}>{1}</button>'

    def render(self):
        attributes = self.attributes.copy()
        if self.value:
            attributes['value'] = str(self.value)
        return self.html.format(flatten_attributes(attributes), self.label.text)

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


class Submit(Input):
    def __init__(self, name, value=None, **kwargs):
        super(Submit, self).__init__(name, value, type='submit', **kwargs)


class File(Input):
    def __init__(self, name, value=None, **kwargs):
        super(File, self).__init__(name, value, type='file', **kwargs)


def flatten_attributes(attrs):
    return ' '.join(['{0}="{1}"'.format(name, value) for name, value in sorted(attrs.items())])
