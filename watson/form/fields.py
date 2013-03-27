# -*- coding: utf-8 -*-
import itertools
from watson.filters.string import Trim
from watson.stdlib.imports import get_qualified_name
from watson.validators.string import Required
# todo: csrf field


class TagMixin(object):
    """Simple tag mixin used for all html tags.

    All keyword arguments that get passed to __init__ will be converted into
    attributes for the element.

    Attributes:
        dict attributes: a dictionary of attributes associated with the tag.
    """
    attributes = None

    def __init__(self, **kwargs):
        self.attributes = {}
        self.attributes.update(kwargs)

    def render(self):
        raise NotImplementedError('The render method has not been implemented')


class Label(TagMixin):
    """A <label> tag which can be automatically included with fields.

    Attributes:
        string html: the html used to render the label
        string text: the text associated with the label
    """
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
    """A mixin that can be used as a base to simplify the creation of fields.

    Attributes:
        watson.form.fields.Label label: the label associated with the field
        string html: the html used to render the field
        list validators: the validators that will be used to validate the value
        list filters: the filters that will be used prior to validation
    """
    _counter = itertools.count()
    label = None
    html = '{0}'
    validators = None
    filters = None
    _errors = None
    _value = None
    _original_value = None

    def __init__(self, name, value=None, label=None, **kwargs):
        """Initializes the field with a specific name.
        """
        self.count = next(FieldMixin._counter)
        self.label = Label(label or name)
        kwargs['name'] = name
        self.value = value
        self.filters = [Trim()] + kwargs.get('filters', [])
        self.validators = kwargs.get('validators', [])
        if 'required' in kwargs:
            self.validators.append(Required())
            kwargs['required'] = 'required'
        self._errors = []
        super(FieldMixin, self).__init__(**kwargs)

    @property
    def value(self):
        """Return the value for the field.

        If the field has been cleaned, the original value can be retrieved
        with FieldMixin.original_value.
        """
        return self._value

    @value.setter
    def value(self, value):
        """Convenience method to set the value on the field.
        """
        self._value = value

    @property
    def original_value(self):
        """Return the original value for the field.
        """
        return self._original_value if self._original_value else self.value

    def filter(self):
        """Filter the value on the field based on the associated filters.

        Set the original_value of the field to the first value stored. Note, if
        this is called a second time, then the original value will be overridden.
        """
        for _filter in self.filters:
            self._original_value = self.value
            self.value = _filter(self.value)

    def validate(self):
        """Validate the value of the field against the associated validators.

        Returns:
            A list of errors that have occurred when the field has been
            validated.
        """
        self._errors = []
        for validator in self.validators:
            try:
                validator(self.value)
            except ValueError as exc:
                self._errors.append(str(exc))
        return self._errors

    @property
    def errors(self):
        return self._errors

    @property
    def name(self):
        """Convenience method to retrieve the name of the field.
        """
        return self.attributes['name']

    def render_with_label(self):
        """Render the field with the label attached.
        """
        raise NotImplementedError('The render method has not been implemented')

    def __str__(self):
        return self.render()

    def __repr__(self):
        return '<{0} name:{1}>'.format(get_qualified_name(self), self.name)


class Input(FieldMixin):
    """Creates an <input> field.

    Custom input types can be created by sending type='type' through the
    __init__ method.

    Usage:
        input = Input(type='text')  # <input type="text" />
    """
    html = '<input {0} />'

    def render(self):
        """Render the element as html.

        Does not need to be called directly, as will be called by __str__
        natively.
        """
        attributes = self.attributes.copy()
        if self.value:
            attributes['value'] = str(self.value)

        return self.html.format(flatten_attributes(attributes))

    def render_with_label(self):
        """Render the element as html and include the label.

        Output the element and prepend the <label> to it.
        """
        return ''.join((self.label.render(self), self.render()))


class GroupInputMixin(Input):
    """A mixin for form elements that are used in a group.

    Related form elements are wrapped in a fieldset, with a common legend.
    """
    label_position = 'left'
    wrapped = True
    values = None
    fieldset_html = '<fieldset><legend>{0}</legend>{1}</fieldset>'

    def __init__(self, name, values=None, value=None, **kwargs):
        super(GroupInputMixin, self).__init__(name, value, **kwargs)
        if not values:
            values = value
        try:
            iter(values)
            self.values = values
        except:
            self.values = [(self.label.text, values)]

    def has_multiple_elements(self):
        """Determine whether or not a field has multiple elements.
        """
        return isinstance(self.values, (tuple, list)) and len(self.values) > 1

    def render(self):
        multiple_elements = self.has_multiple_elements()
        elements = []
        for index, label_value_pair in enumerate(self.values):
            attributes = self.attributes.copy()
            label_text, value = label_value_pair
            if multiple_elements:
                element_id = '{0}_{1}'.format(self.name, index)
            else:
                element_id = self.name
            attributes.update({
                'name': self.name,
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
    """Creates a radio input.

    Usage:
        field = Radio(name='test', label='My Radio Options', values=(('Test', 1), ('Testing', 2)))
        str(field)

        <fieldset>
            <legend>My Radio Options</legend>
            <label for="test_0">Test<input id="test_0" name="test" type="radio" value="1" /></label>
            <label for="test_1">Testing<input id="test_1" name="test" type="radio" value="2" /></label>
        </fieldset>

        field = Radio(name='test', label='My Radio', values=1)
        str(field)
        <label for="test"><input type="radio" name="test" values="1" />My Radio</label>
    """
    def __init__(self, name, values=None, value=None, **kwargs):
        """Initializes the radio.

        If a value is specified, then that value out of the available values will
        be checked.
        If multiple values are specified, then a radio group will be created.

        Args:
            string name: the name of the field
            tuple|list values: the values to be used
            mixed value: the value for the field
        """
        super(Radio, self).__init__(name, values, value, type='radio', **kwargs)


class Checkbox(GroupInputMixin):
    """Creates a checkbox input.

    Usage:
        field = Checkbox(name='test', label='My Radio Options', values=(('Test', 1), ('Testing', 2)))
        str(field)

        <fieldset>
            <legend>My Checkbox Options</legend>
            <label for="test_0">Test<input id="test_0" name="test" type="checkbox" /></label>
            <label for="test_1">Testing<input id="test_1" name="test" type="checkbox" /></label>
        </fieldset>

        field = Checkbox(name='test', label='My Checkbox', values=1)
        str(field)
        <label for="test"><input type="checkbox" name="test" value="1" />My Checkbox</label>
    """
    def __init__(self, name, values=None, value=None, **kwargs):
        """Initializes the checkbox.

        If a value is specified, then that value out of the available values will
        be checked.
        If multiple values are specified, then a checkbox group will be created.

        Args:
            string name: the name of the field
            tuple|list values: the values to be used
            mixed value: the value for the field
        """
        super(Checkbox, self).__init__(name, values, value, type='checkbox', **kwargs)


class Button(Input):
    """Creates a button, can be used instead of Input(type="button").
    """
    html = '<button {0}>{1}</button>'

    def render(self):
        attributes = self.attributes.copy()
        if self.value:
            attributes['value'] = str(self.value)
        return self.html.format(flatten_attributes(attributes), self.label.text)

    def render_with_label(self):
        return self.render()


class Submit(Input):
    """Creates a submit input.

    Attributes:
        bool button_mode: whether or not to render as <button> or <input>
    """
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
    """Creates a textarea field.
    """
    html = '<textarea {0}>{1}</textarea>'

    def render(self):
        attributes = self.attributes.copy()
        value = self.value if self.value else ''
        return self.html.format(flatten_attributes(attributes), value)


class Select(FieldMixin):
    """Creates a select field.

    Attributes:
        string html: the html for the outer select element
        string option_html: the individual option html element
        string optgroup_html: the optgroup html element
        list|dict options: the options available
    """
    html = '<select {0}>{1}</select>'
    option_html = '<option value="{0}"{2}>{1}</option>'
    optgroup_html = '<optgroup label="{0}">{1}</optgroup>'
    options = None

    def __init__(self, name, options=None, value=None, multiple=False, **kwargs):
        """Initializes the select field.

        If the options passed through are a dict, and the value of each key is
        a list or tuple, then an optgroup will be rendered, using the key
        as the label for the optgroup.

        Args:
            string name: the name of the field
            list|dict options: the options available
            string value: the selected value
            bool multiple: whether or not to allow multiple selections

        Usage:
            field = Select(name='test', options=collections.OrderedDict([('Group One', [1, 2]), ('Group Two', [1, 2])]))
            str(field)

            <select name="test">
                <opgroup label="Group One">
                    <option value="1">1</option>
                </optgroup>
                <opgroup label="Group Two">
                    <option value="2">2</option>
                </optgroup>
            </select>
        """
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
        # internal method the render the options
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
        # internal method to render an individual option
        if isinstance(value, (tuple, list)):
            value, label = value
        match = False
        if value == self.value or (isinstance(self.value, (tuple, list)) and value in self.value):
            match = True
        selected = ' selected="selected"' if match else ''
        return self.option_html.format(value, label, selected)

# Convenience classes for input types. Can use Input(type='something') instead
# if required to create a different input field.
# Some of the input types add additional validators and filters to simplify the
# process.


class Text(Input):
    """Creates an <input type="text" /> element.
    """
    def __init__(self, name, value=None, **kwargs):
        super(Text, self).__init__(name, value, type='text', **kwargs)


class Date(Input):
    """Creates an <input type="date" /> element.
    """
    def __init__(self, name, value=None, **kwargs):
        super(Date, self).__init__(name, value, type='date', **kwargs)


class Email(Input):
    """Creates an <input type="email" /> element.
    """
    def __init__(self, name, value=None, **kwargs):
        super(Email, self).__init__(name, value, type='email', **kwargs)


class Hidden(Input):
    """Creates an <input type="hidden" /> element.
    """
    def __init__(self, name, value=None, **kwargs):
        super(Hidden, self).__init__(name, value, type='hidden', **kwargs)


class Password(Input):
    """Creates an <input type="password" /> element.
    """
    def __init__(self, name, value=None, **kwargs):
        super(Password, self).__init__(name, value, type='password', **kwargs)


class File(Input):
    def __init__(self, name, value=None, **kwargs):
        super(File, self).__init__(name, value, type='file', **kwargs)


def flatten_attributes(attrs):
    """Flattens attributes into a single string of key=value pairs.

    Attributes are sorted alphabetically.
    """
    return ' '.join(['{0}="{1}"'.format(name, value) for name, value in sorted(attrs.items())])
