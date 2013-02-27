# -*- coding: utf-8 -*-
from watson.form.fields import FieldMixin, flatten_attributes
from watson.stdlib.imports import get_qualified_name


class Form(FieldMixin):
    attributes = None

    @property
    def method(self):
        return self.attributes['method']

    @property
    def action(self):
        return self.attributes['action']

    @property
    def enctype(self):
        return self.attributes['enctype']

    @property
    def elements(self):
        return [element for element in dir(self) if not element.startswith('__') and isinstance(element, FieldMixin)]

    def __init__(self, name, method='post', action=None, **kwargs):
        self.attributes = {}
        self.attributes.update(kwargs)
        self.attributes.update({
            'name': name,
            'method': method,
            'action': kwargs.get('action', '/'),
            'enctype': kwargs.get('enctype', 'application/x-www-form-urlencoded')
        })

    @property
    def errors(self):
        pass  # todo, call validate first

    def begin(self):
        return '<form {0}>'.format(flatten_attributes(self.attributes))

    def end(self):
        return '</form>'

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return '<{0} name:{1} method:{2} action:{3}>'.format(
                    get_qualified_name(self),
                    self.name,
                    self.method,
                    self.action)


class MultipartForm(Form):
    """
    Purely a convenience class for forms that have an encoding type of multipart/form-data.
    """
    def __init__(self, name, method='post', action=None, **kwargs):
        kwargs['enctype'] = 'multipart/form-data'
        super(MultipartForm, self).__init__(name, method, action, **kwargs)
