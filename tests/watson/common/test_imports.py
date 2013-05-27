# -*- coding: utf-8 -*-
import imp
import sys
from watson.common.imports import get_qualified_name, load_definition_from_string, Resolver
from tests.watson.common.support import some_func
import tests.watson.common


class TestImports(object):
    def test_qualified_name(self):
        assert 'tests.watson.common.test_imports.TestImports' == get_qualified_name(self)
        assert 'tests.watson.common.support.some_func' == get_qualified_name(some_func)

    def test_load_definition_from_string(self):
        assert isinstance(load_definition_from_string('watson.http.MIME_TYPES'), dict)

    def test_load_invalid_definition(self):
        assert None == load_definition_from_string('invalid.module.Class')


class TestResolver(object):
    def test_resolver_registration(self):
        resolver = Resolver('test')
        assert resolver in sys.meta_path
        resolver.deregister()
        assert resolver not in sys.meta_path

    def test_find_module(self):
        resolver = Resolver('test')
        result = resolver.find_module('test.module')
        assert result == resolver
        result = resolver.find_module('something')
        assert not result

    def test_module_repr(self):
        resolver = Resolver()
        repr_str = resolver.module_repr(tests.watson.common)
        assert repr_str.startswith("<module 'tests.watson.common'")

    def test_load_package(self):
        resolver = Resolver('testing')
        module = imp.new_module('testing_something')
        module.__file__ = 'testing_something.py'
        sys.modules['testing_something'] = module
        loaded = resolver.load_module('testing.something')
        assert module == loaded
        assert resolver.module_repr(loaded).endswith("aliased by 'testing.something'>'")

    def test_load_nested_packages(self):
        resolver = Resolver('testing')
        module = imp.new_module('nested_testing.something.else')
        module.__file__ = 'nested_testing/something/else.py'
        sys.modules['nested_testing.something.else'] = module
        loaded = resolver.load_module('nested.testing.something.else')
        assert module == loaded
        assert resolver.module_repr(loaded).endswith("aliased by 'nested.testing.something.else'>'")

    def test_load_module(self):
        resolver = Resolver('testing')
        module = imp.new_module('testing')
        module.__file__ = 'testing.py'
        sys.modules['testing'] = module
        loaded = resolver.load_module('testing')
        assert module == loaded
        assert resolver.module_repr(loaded) == "<module 'testing' from 'testing.py'>'"
