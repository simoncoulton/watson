# -*- coding: utf-8 -*-
from uuid import uuid4
import hashlib
from watson.common.datastructures import MultiDict
from watson.form import fields
from watson import validators


def has_csrf(cls):
    """Adds csrf protection to the form.

    Adds a new field named 'csrf_token' to the form and overrides the
    set data method to retrieve the correct token.

    If a form is csrf protected then a session object must be passed to
    the __init__ method so that a token can be created (if not already).

    Usage:
        @has_csrf
        class MyForm(Form):
            username = fields.Text(required=True)
            password = fields.Password(required=True)
    """
    class CsrfProtectedForm(cls):
        csrf_token = fields.Csrf()

        def __init__(self, name, method='post', action=None, detect_multipart=True, session=None, **kwargs):
            """Inititalize the form and set some default attributes.

            Args:
                string name: the name of the form
                string method: the http method to use
                string action: the url to submit the form to
                boolean detect_multipart: automatically set multipart/form-data
                watson.http.session.StorageMixin session: the session in which to store the token
            """
            if not session:
                raise ValueError('A session must be assigned to the form for validation.')
            super(CsrfProtectedForm, self).__init__(name, method, action, detect_multipart, **kwargs)
            token_name = '{0}_csrf_token'.format(self.name)
            if token_name not in session or not session.get(token_name):
                token = '{0}{1}{2}'.format(token_name, uuid4().hex, session.id)
                actual = hashlib.sha256(token.encode('utf-8')).hexdigest()
                session[token_name] = actual
            for validator in self.csrf_token.validators:
                if isinstance(validator, validators.Csrf):
                    validator.token = session[token_name]
            self.csrf_token.value = session[token_name]

        @property
        def data(self):
            # required for the setter override
            return super(CsrfProtectedForm, self).data

        @data.setter
        def data(self, data):
            """Sets the data for the form.

            Override the existing set data method and inject the csrf
            token into the form.
            """
            token_name = '{0}_csrf_token'.format(self.name)
            if hasattr(data, 'post'):
                raw_data = MultiDict()
                for key, value in data.files.items():
                    raw_data[key] = value
                for key, value in data.post.items():
                    if key.endswith('_csrf_token'):
                        raw_data['csrf_token'] = value
                    else:
                        raw_data[key] = value
            else:
                if token_name in data:
                    data['csrf_token'] = data[token_name]
                    del data[token_name]
                raw_data = data
            self._set_data_on_fields(raw_data)

        def close(self):
            """Render the end tag of the form.

            Automatically renders the csrf field within the form.
            """
            return '{0}{1}'.format(self.csrf_token, super(CsrfProtectedForm, self).close())

    return CsrfProtectedForm
