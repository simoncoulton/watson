# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.common.datastructures import ImmutableDict, ImmutableMultiDict
from watson.common.datastructures import MultiDict, dict_deep_update
from copy import copy, deepcopy


class TestImmutableDict(object):
    def test_create(self):
        d = ImmutableDict({'test': 'blah', 'something': '2'})
        assert d.__len__() == 2

    def test_copy(self):
        d = ImmutableDict({'test': 'blah', 'something': '2'})
        c = copy(d)
        c['blah'] = 'blah'
        assert d != c

    @raises(TypeError)
    def test_set_value(self):
        d = ImmutableDict()
        d['something'] = 'test'


class TestImmutableMultiDict(object):
    def test_create(self):
        d = ImmutableMultiDict({'test': 'blah', 'something': '2'})
        assert d.__len__() == 2

    @raises(TypeError)
    def test_set_value(self):
        d = ImmutableMultiDict()
        d['something'] = 'test'

    @raises(TypeError)
    def test_del_value(self):
        d = ImmutableMultiDict()
        d['something'] = 'test'
        print('here')
        del d['something']

    def test_copy(self):
        d = ImmutableMultiDict({'test': 'blah', 'something': '2'})
        d2 = copy(d)
        assert d == d2

    def test_deep_copy(self):
        d = ImmutableMultiDict({'test': 'blah', 'something': '2'})
        d2 = deepcopy(d)
        assert d == d2


class TestMultiDict(object):
    def test_add_key(self):
        d = MultiDict({'test': 'blah', 'something': '2'})
        d['test'] = 'something'
        d['another'] = ['b']
        d['another'] = 'c'
        assert d['test'].__len__() == 2


class TestFunctions(object):
    def test_dict_deep_update(self):
        d1 = {'a': {'b': 3}}
        d2 = {'a': {'b': 4}}
        merged = dict_deep_update(d1, d2)
        assert merged['a']['b'] == 4

    def test_dict_deep_update_not_dict(self):
        d1 = {'a': {'b': 3}}
        d2 = 'b'
        merged = dict_deep_update(d1, d2)
        assert merged == 'b'
