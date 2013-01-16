# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.di.container import IocContainer


class TestIoc(object):
    def test_create_container(self):
        container = IocContainer()
        assert container.__repr__() == '<watson.di.container.IocContainer: 0 param(s), 0 definition(s)>'
        assert container.params == {}
        assert container.definitions == {}

    def test_get_item(self):
        container = IocContainer({
            'definitions': {
                'test': {
                    'item': 'tests.watson.di.test_container.SampleDependency',
                    'type': 'singleton',
                },
                'test2': {
                    'item': 'tests.watson.di.test_container.sample_dependency',
                    'type': 'singleton',
                }
            }
        })
        container.add('def', lambda container: 'something')
        assert isinstance(container.get('test'), SampleDependency)
        assert container.get('test2') == 'test'
        assert container.get('def') == 'something'
        assert container.get('def') == 'something'

    def test_add_item(self):
        container = IocContainer()
        container.add('dep', lambda container: 'something')
        assert container.get('dep') == 'something'

    def test_add_instantiated(self):
        container = IocContainer()
        dep = SampleDependency()
        container.add('dep', dep)
        assert container.get('dep') == dep

    def test_add_dict(self):
        container = IocContainer()
        dep = {'something': 'test'}
        container.add('dep', dep)
        assert container.get('dep') == dep

    @raises(KeyError)
    def test_definition_doesnt_exist(self):
        container = IocContainer()
        container.get('test')

    @raises(KeyError)
    def test_definition_item_doesnt_exist(self):
        container = IocContainer({
            'definitions': {
                'test': {}
            }
        })
        container.get('test')

    @raises(TypeError)
    def test_attach_invalid_processor(self):
        container = IocContainer()
        container.attach_processor('event.container.pre', 'test')

    def test_prototype(self):
        container = IocContainer({
            'definitions': {
                'test': {
                    'item': 'tests.watson.di.test_container.SampleDependency',
                    'type': 'prototype'
                }
            }
        })
        test1 = container.get('test')
        test2 = container.get('test')
        assert test1 != test2


def sample_dependency(container):
    return 'test'


class SampleDependency(object):
    pass
