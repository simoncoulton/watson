# -*- coding: utf-8 -*-
# Support functions, classes
from watson.form import Form, fields


form_user_mapping = {'first_name': ('personal', 'first_name'), 'email': ('personal', 'contact', 'email')}


class LoginForm(Form):
    username = fields.Text(name='username', required=True)
    password = fields.Password(name='password', required=True)
    first_name = fields.Text(name='first_name')
    last_name = fields.Text(name='last_name')
    email = fields.Text(name='email')


class UploadForm(Form):
    image = fields.File(name='upload_image')


class Other(object):
    test = None


class Contact(object):
    email = None


class Personal(object):
    first_name = None
    last_name = None
    contact = None

    def __init__(self):
        self.contact = Contact()


class User(object):
    id = None
    username = None
    password = None
    personal = None

    def __init__(self, username=None, password=None):
        self.personal = Personal()
        if username:
            self.username = username
        if password:
            self.password = password

    def __repr__(self):
        return '<User username:{0} password:{1}>'.format(self.username, self.password)
