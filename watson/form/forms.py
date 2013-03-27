# -*- coding: utf-8 -*-
import collections
from copy import deepcopy
from watson.form.fields import FieldMixin, TagMixin, File, flatten_attributes
from watson.stdlib.decorators import cached_property
from watson.stdlib.imports import get_qualified_name


class Form(TagMixin):
    """A basic

    """
    attributes = None
    validated = False
    valid = False
    _ignored_attributes = ('fields', '_fields', 'data', 'raw_data', 'errors')
    _bound_object = None
    _bound_object_mapping = None

    def __init__(self, name, method='post', action=None, detect_multipart=True, **kwargs):
        """Inititalize the form and set some default attributes.
        """
        self.attributes = {}
        self.attributes.update(kwargs)
        self.attributes.update({
            'name': name,
            'method': method,
            'action': kwargs.get('action', '/'),
            'enctype': kwargs.get('enctype', 'application/x-www-form-urlencoded')
        })
        for field_name, field in self.fields.items():
            # create a copy of the field so that we're not referencing
            # the class attr of the same name.
            if detect_multipart and isinstance(field, File):
                self.attributes['enctype'] = 'multipart/form-data'
            setattr(self, field_name, deepcopy(field))
        del self._fields

    @cached_property
    def fields(self):
        """Retrieve a list of all fields associated with the form.

        Fields are sorted based on the order that they are defined in so that
        error messages can be displayed in the correct order.
        The list of fields is cached so that it is only required to be read once.
        If the cache needs to be cleared, the _fields attribute can be deleted.

        Returns:
            OrderedDict of fields.
        """
        fields = []
        for field_name in dir(self):
            if field_name not in self._ignored_attributes and not field_name.startswith('_'):
                # ignore properties for recursion
                field = getattr(self, field_name)
                if isinstance(field, FieldMixin):
                    fields.append((field_name, field))
        fields.sort(key=lambda pair: pair[1].count)
        return collections.OrderedDict(fields)

    @cached_property
    def errors(self):
        """Returns a list of errors associated with the form.

        If the form has not been validated yet, calling this property
        will cause validation to occur.
        """
        self.is_valid()
        errors = {}
        for field_name, field in self.fields.items():
            error_list = field.errors
            if error_list:
                errors[field_name] = {'messages': field.errors,
                                      'label': field.label.text}
        return errors

    @cached_property
    def data(self):
        """Returns a dict containing all the field values.

        Used as a shorthand method to retrieve data from all the form fields
        rather than having to access the fields themselves.
        """
        return {field_name: field.value for
                field_name, field in self.fields.items()}

    @cached_property
    def raw_data(self):
        """Returns a dict containing all the original field values.

        Field values will be their pre-filtered values.
        """
        return {field_name: field.original_value for
                field_name, field in self.fields.items()}

    def bind(self, data, obj=None):
        self.invalidate()
        for field, value in data.items():
            if field in self.fields:
                self.fields[field].value = value

    # validation methods

    def invalidate(self):
        try:
            del self._data
        except AttributeError:
            pass
        try:
            del self._raw_data
        except AttributeError:
            pass
        try:
            del self._errors
        except AttributeError:
            pass
        self.validated = self.valid = False

    def is_valid(self):
        if not self.validated:
            self.valid = True
            for field_name, field in self.fields.items():
                field.filter()
                valid = field.validate()
                if not valid:
                    self.valid = False
            self.validated = True
        return self.valid

        # loop thru fields and validate each one
        # if fail validation self.valid = False
        # if self.valid and self._bound_object:
        #     self._hydrate_data_to_object(self._bound_object, self.data, self._bound_object_mapping)

    # rendering methods

    def begin(self):
        return '<form {0}>'.format(flatten_attributes(self.attributes))

    def end(self):
        return '</form>'

    # convenience methods

    @property
    def name(self):
        """Convenience method to retrieve the name of the field.
        """
        return self.attributes['name']

    @property
    def method(self):
        return self.attributes['method']

    @property
    def action(self):
        return self.attributes['action']

    @property
    def enctype(self):
        return self.attributes['enctype']

    # def bind(self, obj, mapping=None, hydrate_form=True):
    #     self.invalidate()
    #     self._bound_object = obj
    #     self._bound_object_mapping = mapping
    #     if hydrate_form:
    #         self.data = self._hydrate_object_to_form_data(self._bound_object, self.data, self._bound_object_mapping)

    # def _hydrate_object_to_form_data(self, obj=None, data=None, mapping=None):
    #     if not obj:
    #         raise AttributeError('Object cannot be bound to form "{0}"'.format(self.name))
    #     obj_mapping = mapping if mapping else []
    #     for field in self.fields:
    #         try:
    #             field_value = getattr(obj, field.name)
    #             if field_value:
    #                 data[field.name] = field_value
    #                 field.value = field_value
    #         except:
    #             pass
    #         if field.name in obj_mapping:
    #             last_field = obj_mapping[field.name][-1]
    #             current_obj = obj
    #             for field_name in obj_mapping[field.name][0:-1]:
    #                 current_obj = getattr(current_obj, field_name)
    #             try:
    #                 field_value = getattr(current_obj, last_field)
    #                 if field_value:
    #                     data[last_field] = field_value
    #                     field.value = field_value
    #             except:
    #                 pass

    # def _hydrate_data_to_object(self, obj=None, data=None, mapping=None):
    #     if not obj:
    #         raise AttributeError('No object has been bound to form "{0}"'.format(self.name))
    #     obj_mapping = mapping if mapping else []
    #     for name, value in data.items():
    #         if name in obj_mapping:
    #             last_field = obj_mapping[name][-1]
    #             current_obj = obj
    #             for field_name in obj_mapping[name][0:-1]:
    #                 current_obj = getattr(current_obj, field_name)
    #             setattr(current_obj, last_field, value)
    #         elif hasattr(obj, name):
    #             setattr(obj, name, value)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return '<{0} name:{1} method:{2} action:{3} fields:{4}>'.format(
            get_qualified_name(self),
            self.name,
            self.method,
            self.action,
            len(self))


class MultipartForm(Form):
    """Convenience class for forms that should be multipart/form-data.

    By default, the Form class will automatically detect whether or not
    a field is of type file, and convert it to multipart.
    """
    def __init__(self, name, method='post', action=None, **kwargs):
        kwargs['enctype'] = 'multipart/form-data'
        super(MultipartForm, self).__init__(name, method, action, **kwargs)
