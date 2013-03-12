# -*- coding: utf-8 -*-
# Support functions, classes
from watson.form import Form, fields


class LoginForm(Form):
    username = fields.Text(name='username')
    password = fields.Password(name='password')
    first_name = fields.Text(name='first_name')
    last_name = fields.Text(name='last_name')


class Personal:
    first_name = None
    last_name = None


class User:
    id = None
    username = None
    password = None
    personal = Personal()
