# -*- coding: utf-8 -*-
from io import BytesIO, BufferedReader
from nose.tools import raises
from watson.form.decorators import has_csrf
from watson.http.messages import create_request_from_environ
from tests.watson.form.support import UnprotectedForm, sample_environ


class TestHasCsrf(object):
    def setup(self):
        self.protected_form = has_csrf(UnprotectedForm)
        environ = sample_environ(REQUEST_METHOD='POST')
        environ['wsgi.input'] = BufferedReader(BytesIO(b'test=blah'))
        self.request = create_request_from_environ(environ, 'watson.http.sessions.Memory')

    def test_add_csrf_field_to_form(self):
        assert not hasattr(UnprotectedForm, 'csrf_token')
        assert hasattr(self.protected_form, 'csrf_token')

    @raises(ValueError)
    def test_create_form_no_session(self):
        self.protected_form('test')

    def test_create_token(self):
        form = self.protected_form('test', session=self.request.session)
        assert 'test_csrf_token' in self.request.session
        assert form.data['csrf_token'] == self.request.session['test_csrf_token']

    def test_use_existing_token(self):
        self.request.session['test_csrf_token'] = '12345'
        form = self.protected_form('test', session=self.request.session)
        assert form.data['csrf_token'] == '12345'

    def test_set_data_from_request(self):
        form = self.protected_form('test', session=self.request.session)
        form.data = self.request
        assert form.data['test'] == 'blah'

    def test_set_data_from_dict(self):
        form = self.protected_form('test', session=self.request.session)
        form.data = {'test_csrf_token': 'blah'}
        assert form.data['csrf_token'] == 'blah'

    def test_form_closing_tag(self):
        form = self.protected_form('test', session=self.request.session)
        tag = form.close()
        assert tag[:24] == '<input name="csrf_token"'
        assert tag[-7:] == '</form>'
