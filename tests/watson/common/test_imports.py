# -*- coding: utf-8 -*-
from watson.common.imports import get_qualified_name, load_definition_from_string
from tests.watson.common.support import some_func


class TestImports(object):
    def test_qualified_name(self):
        assert 'tests.watson.common.test_imports.TestImports' == get_qualified_name(self)
        assert 'tests.watson.common.support.some_func' == get_qualified_name(some_func)

    def test_load_definition_from_string(self):
        assert isinstance(load_definition_from_string('watson.http.MIME_TYPES'), dict)

    def test_load_invalid_definition(self):
        assert None == load_definition_from_string('invalid.module.Class')
