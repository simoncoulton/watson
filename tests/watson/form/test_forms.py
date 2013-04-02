# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.form import Form, MultipartForm
from tests.watson.form.support import LoginForm, UploadForm, User, form_user_mapping, Contact, Other


class TestForm(object):
    def test_form_create(self):
        form = Form('test')
        assert len(form) == 0
        assert len(form.fields) == 0
        assert repr(form) == '<watson.form.forms.Form name:test method:post action:/ fields:0>'
        form2 = LoginForm('test')
        assert len(form2) == 5

    def test_form_start_tag(self):
        form = Form('test')
        assert form.open() == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test">'

    def test_form_end_tag(self):
        form = Form('test')
        assert form.close() == '</form>'

    def test_set_data_on_form(self):
        form = LoginForm('test')
        post_data = {'username': 'simon', 'password': 'test', 'first_name': None, 'last_name': None, 'email': None}
        form.data = post_data
        assert form.data == post_data

    def test_bind_object_to_form_with_mapping(self):
        form = LoginForm('test')
        user = User(username='simon', password='test')
        user.personal.first_name = 'Simon'
        user.personal.contact.email = 'simon.coulton@gmail.com'
        form.bind(user, form_user_mapping)
        assert form.username.value == 'simon'
        assert form.first_name.value == 'Simon'
        assert form.email.value == 'simon.coulton@gmail.com'
        assert form.password.value == 'test'
        form.data = {'password': 'newpass'}
        assert form.password.value == 'newpass'

    def test_hydrate_form_to_object_with_mapping(self):
        form = LoginForm('test')
        form.data = {'username': 'simon', 'password': 'test', 'email': 'simon.coulton@gmail.com'}
        user = User()
        form.bind(user, form_user_mapping, hydrate=False)
        form.is_valid()
        assert user.username == 'simon'
        assert user.password == 'test'
        assert user.personal.contact.email == 'simon.coulton@gmail.com'

    def test_bind_object_to_form_without_mapping(self):
        form = LoginForm('test')
        user = User(username='simon', password='test')
        form.bind(user)
        assert form.username.value == 'simon'
        assert form.password.value == 'test'
        form.data = {'password': 'newpass'}
        assert form.password.value == 'newpass'

    def test_hydrate_form_to_object_without_mapping(self):
        form = LoginForm('test')
        form.data = {'username': 'simon', 'password': 'test'}
        user = User()
        form.bind(user, hydrate=False)
        form.is_valid()
        assert user.username == 'simon'
        assert user.password == 'test'

    @raises(AttributeError)
    def test_hydrate_form_to_object_with_mapping_invalid_class(self):
        form = LoginForm('test')
        form.data = {'username': 'simon', 'password': 'test'}
        user = Contact()  # obviously not a user
        form.bind(user, {'username': ('firstname', 'test')}, hydrate=False)
        form.is_valid()

    @raises(AttributeError)
    def test_hydrate_object_with_mapping_invalid_class(self):
        form = LoginForm('test')
        user = Other()
        user.test = 'test'
        form.bind(user, {'username': ('blah', 'field')})

    def test_alter_form_multipart(self):
        form = UploadForm('test')
        assert form.enctype == 'multipart/form-data'

    def test_setting_raw_data(self):
        form = LoginForm('test')
        data = {'username': 'simon'}
        expected_data = {'first_name': None, 'last_name': None, 'password': None, 'username': 'simon', 'email': None}
        form.data = data
        assert form.username.value == 'simon'
        assert form.data == expected_data
        assert form.raw_data == expected_data

    def test_filter_and_validate_input(self):
        form = LoginForm('test')
        data = {'username': 'simon '}
        form.data = data
        form.is_valid()
        assert form.username.value == 'simon'
        assert form.username.original_value == 'simon '
        assert form.errors == {'password': {'messages': ['Value is required'], 'label': 'password'}}


class TestMultiPartForm(object):
    def test_multi_part(self):
        form = MultipartForm('test')
        assert form.enctype == 'multipart/form-data'

    def test_form_start_tag(self):
        form = MultipartForm('test')
        assert form.open() == '<form action="/" enctype="multipart/form-data" method="post" name="test">'
