# -*- coding: utf-8 -*-
from watson.form import Form, MultipartForm


class TestForm(object):
    def test_form_create(self):
        form = Form('test')
        assert len(form) == 0
        assert len(form.elements) == 0
        assert repr(form) == '<watson.form.forms.Form name:test method:post action:/>'

    def test_form_start_tag(self):
        form = Form('test')
        assert form.begin() == '<form action="/" enctype="application/x-www-form-urlencoded" method="post" name="test">'

    def test_form_end_tag(self):
        form = Form('test')
        assert form.end() == '</form>'


class TestMultiPartForm(object):
    def test_multi_part(self):
        form = MultipartForm('test')
        assert form.enctype == 'multipart/form-data'
