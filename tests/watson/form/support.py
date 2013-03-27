# -*- coding: utf-8 -*-
# Support functions, classes
from watson.form import Form, fields


class LoginForm(Form):
    username = fields.Text(name='username', required=True)
    password = fields.Password(name='password', required=True)
    first_name = fields.Text(name='first_name')
    last_name = fields.Text(name='last_name')


class UploadForm(Form):
    image = fields.File(name='upload_image')


class Personal(object):
    first_name = None
    last_name = None


class User(object):
    id = None
    username = None
    password = None
    personal = Personal()
