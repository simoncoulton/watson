# -*- coding: utf-8 -*-
from watson.form.fields import FieldMixin, flatten_attributes
from watson.stdlib.imports import get_qualified_name


class Form(FieldMixin):
    attributes = None
    validated = False
    valid = False
    _data = None
    _validated_data = None
    _bound_object = None
    _bound_object_mapping = None

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
        return [getattr(self, element) for element in dir(self) if not element.startswith('__') \
                                                 and not element == 'elements' \
                                                 and isinstance(getattr(self, element), FieldMixin)]

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
        self.is_valid()

    @property
    def data(self):
        return self._validated_data if self.validated and self.valid else self._data

    @data.setter
    def data(self, data):
        self.invalidate()
        self._data = data

    def bind(self, obj, mapping=None):
        self.invalidate()
        self._bound_object = obj
        self._bound_object_mapping = mapping

    def invalidate(self):
        self.validated = False

    def is_valid(self):
        if not self.validated:
            self._validate()
        return self.valid

    def begin(self):
        return '<form {0}>'.format(flatten_attributes(self.attributes))

    def end(self):
        return '</form>'

    def _validate(self):
        self.valid = False

    def _hydrate_data_to_object(self, obj=None, data=None, mapping=None):
        if not obj:
            raise AttributeError('No object has been bound to form "{0}"'.format(self.name))
        obj_mapping = mapping if mapping else []
        for name, value in data.items():
            if name in obj_mapping:
                last_field = obj_mapping[name][-1]
                current_obj = obj
                for field_name in obj_mapping[name][0:-1]:
                    current_obj = getattr(current_obj, field_name)
                setattr(current_obj, last_field, value)
            elif hasattr(obj, name):
                setattr(obj, name, value)

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return '<{0} name:{1} method:{2} action:{3} fields:{4}>'.format(
                    get_qualified_name(self),
                    self.name,
                    self.method,
                    self.action,
                    len(self))


class MultipartForm(Form):
    """
    Purely a convenience class for forms that have an encoding type of multipart/form-data.
    """
    def __init__(self, name, method='post', action=None, **kwargs):
        kwargs['enctype'] = 'multipart/form-data'
        super(MultipartForm, self).__init__(name, method, action, **kwargs)
