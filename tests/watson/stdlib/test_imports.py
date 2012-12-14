# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.stdlib.imports import get_qualified_name, load_definition_from_string


class TestImports(object):
    def test_qualified_name(self):
        assert 'tests.watson.stdlib.test_imports.TestImports' == get_qualified_name(self)

    def test_load_definition_from_string(self):
        assert isinstance(load_definition_from_string('watson.http.MIME_TYPES'), dict)

    def test_load_invalid_definition(self):
        assert None == load_definition_from_string('invalid.module.Class')
