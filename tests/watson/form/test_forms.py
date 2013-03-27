# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.form import Form, MultipartForm
from tests.watson.form.support import LoginForm, UploadForm, User


class TestForm(object):
    def test_form_create(self):
        form = Form('test')
        assert len(form) == 0
        assert len(form.fields) == 0
        assert repr(form) == '<watson.form.forms.Form name:test method:post action:/ fields:0>'
        form2 = LoginForm('test')
        assert len(form2) == 4

    def test_form_start_tag(self):
        form = Form('test')
        assert form.begin() == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test">'

    def test_form_end_tag(self):
        form = Form('test')
        assert form.end() == '</form>'

    def test_set_data_on_form(self):
        form = LoginForm('test')
        post_data = {'username': 'simon', 'password': 'test', 'first_name': None, 'last_name': None}
        form.bind(post_data)
        assert form.data == post_data

    # def test_bind_object_and_mapping(self):
    #     form = LoginForm('test')
    #     user = User()
    #     mapping = {'first_name': ('personal', 'first_name'), 'last_name': ('personal', 'last_name')}
    #     form.bind(user, mapping)
    #     assert form._bound_object == user
    #     assert form._bound_object_mapping == mapping

    # def test_hydrate_object_to_form_data(self):
    #     form = LoginForm('test')
    #     user = User()
    #     user.username = 'simon'
    #     user.password = 'test'
    #     user.personal.first_name = 'Simon'
    #     user.personal.last_name = 'Coulton'
    #     mapping = {'first_name': ('personal', 'first_name'), 'last_name': ('personal', 'last_name')}
    #     form.bind(user, mapping)
    #     assert form.username.value == 'simon'
    #     assert form.first_name.value == 'Simon'

    # def test_hydrate_form_data_to_object(self):
    #     form = LoginForm('test')
    #     user = User()
    #     post_data = {'username': 'simon', 'password': 'test', 'first_name': 'Simon', 'last_name': 'Coulton'}
    #     mapping = {'first_name': ('personal', 'first_name'), 'last_name': ('personal', 'last_name')}
    #     form._hydrate_data_to_object(user, post_data, mapping)
    #     assert user.username == 'simon'
    #     assert user.password == 'test'
    #     assert user.personal.first_name == 'Simon'
    #     assert user.personal.last_name == 'Coulton'

    # @raises(AttributeError)
    # def test_bind_form_data_to_object_no_object(self):
    #     form = LoginForm('test')
    #     form._hydrate_data_to_object()
    def test_alter_form_multipart(self):
        form = UploadForm('test')
        assert form.enctype == 'multipart/form-data'

    def test_setting_raw_data(self):
        form = LoginForm('test')
        data = {'username': 'simon'}
        expected_data = {'first_name': None, 'last_name': None, 'password': None, 'username': 'simon'}
        form.bind(data)
        assert form.username.value == 'simon'
        assert form.data == expected_data
        assert form.raw_data == expected_data

    def test_filter_and_validate_input(self):
        form = LoginForm('test')
        data = {'username': 'simon '}
        form.bind(data)
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
        assert form.begin() == '<form action="/" enctype="multipart/form-data" method="post" name="test">'
