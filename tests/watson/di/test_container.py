# -*- coding: utf-8 -*-
from watson.di.container import IocContainer


class TestIoc(object):
    def test_create_container(self):
        container = IocContainer()
        assert container.__repr__() == '<watson.di.container.IocContainer: 0 param(s), 0 definition(s)>'

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

    def test_add_item(self):
        container = IocContainer()
        container.add('def', lambda container: 'something')
        assert container.get('def') == 'something'


def sample_dependency(container):
    return 'test'


class SampleDependency(object):
    pass
