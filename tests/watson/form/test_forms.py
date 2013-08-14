# -*- coding: utf-8 -*-
from io import BytesIO, BufferedReader
from nose.tools import raises
from watson.form import Form, Multipart
from watson.http.messages import create_request_from_environ, Request
from tests.watson.form.support import LoginForm, UploadForm, User, form_user_mapping, Contact, Other, sample_environ, ProtectedForm, SampleFormValidator


class TestForm(object):

    def test_form_create(self):
        form = Form('test')
        assert len(form) == 0
        assert len(form.fields) == 0
        assert repr(
            form) == '<watson.form.forms.Form name:test method:post action:/ fields:0>'
        form2 = LoginForm('test')
        assert len(form2) == 5

    def test_form_create_no_name(self):
        form = Form()
        assert form.name == 'Form'
        login_form = LoginForm()
        assert login_form.name == 'LoginForm'

    def test_form_start_tag(self):
        form = Form('test')
        assert form.open(
        ) == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test">'

    def test_form_end_tag(self):
        form = Form('test')
        assert form.close() == '</form>'

    def test_set_data_on_form(self):
        form = LoginForm('test')
        post_data = {
            'username': 'simon',
            'password': 'test',
            'first_name': None,
            'last_name': None,
            'email': None}
        form.data = post_data
        assert form.data == post_data
        request = Request(
            'GET',
            post={'first_name': 'data'},
            files={'file': 'something'})
        form.data = request
        assert form.data['first_name'] == 'data'

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
        form.data = {
            'username': 'simon',
            'password': 'test',
            'email': 'simon.coulton@gmail.com'}
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
        expected_data = {
            'first_name': None,
            'last_name': None,
            'password': None,
            'username': 'simon',
            'email': None}
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
        assert form.errors == {
            'password': {
                'messages': [
                    'Value is required'],
                'label': 'password'}}

    def test_validate_form_success(self):
        form = LoginForm(validators=[SampleFormValidator()])
        form.data = {'username': 'Simon', 'password': 'Test'}
        valid = form.is_valid()
        assert valid

    def test_validate_form_invalid(self):
        form = LoginForm(validators=[SampleFormValidator()])
        form.data = {'username': 'Simone', 'password': 'test'}
        valid = form.is_valid()
        assert not valid
        assert form.errors == {'form': {'messages': ['Username does not match.'], 'label': 'Form'}}

    def test_render_entire_form(self):
        form = LoginForm('test')
        rendered_form = str(form)
        assert rendered_form == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test"><div><label for="username">username</label><input id="username" name="username" required="required" type="text" /></div><div><label for="password">password</label><input id="password" name="password" required="required" type="password" /></div><div><label for="first_name">first_name</label><input id="first_name" name="first_name" type="text" /></div><div><label for="last_name">last_name</label><input id="last_name" name="last_name" type="text" /></div><div><label for="email">email</label><input id="email" name="email" type="text" /></div></form>'

    def test_custom_method(self):
        form = LoginForm('test', method='PUT')
        assert form.http_request_method.value == 'PUT'
        assert form.close(
        ) == '<input name="HTTP_REQUEST_METHOD" type="hidden" value="PUT" /></form>'


class TestMultiPartForm(object):

    def test_multi_part(self):
        form = Multipart('test')
        assert form.enctype == 'multipart/form-data'

    def test_form_start_tag(self):
        form = Multipart('test')
        assert form.open(
        ) == '<form action="/" enctype="multipart/form-data" method="post" name="test">'
        assert form.open(action='/put') == '<form action="/put" enctype="multipart/form-data" method="post" name="test">'


class TestFormProcessingCsrfRequest(object):

    def setup(self):
        environ = sample_environ(
            HTTP_COOKIE='watson.session=123456;',
            REQUEST_METHOD='POST')
        environ['wsgi.input'] = BufferedReader(
            BytesIO(b'form_csrf_token=123456&test=blah'))
        self.request = create_request_from_environ(
            environ, 'watson.http.sessions.Memory')

    def teardown(self):
        self.request.session.destroy()
        del self.request

    def test_valid_csrf_token(self):
        self.request.session['form_csrf_token'] = '123456'
        form = ProtectedForm('form', session=self.request.session)
        form.data = self.request
        valid = form.is_valid()
        assert valid

    def test_invalid_csrf_token(self):
        form = ProtectedForm('form', session=self.request.session)
        form.data = self.request
        valid = form.is_valid()
        assert not valid
