# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.di import processors
from watson.di.container import IocContainer
from watson.events.types import Event
from tests.watson.di.support import sample_dependency, SampleDependencyAware, SampleProcessor


def sample_event(target):
    definition = {
        'item': target,
    }
    return Event('Sample',
                 params={
                     'definition': definition
                 },
                 target=definition)


class TestConstructorInjection(object):

    def test_inject_value_dict(self):
        processor = processors.ConstructorInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.target['init'] = {'sample': 'test'}
        instance = processor(event)
        assert instance.first_kw == 'test'

    def test_inject_value_list(self):
        processor = processors.ConstructorInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.target['init'] = ['test']
        instance = processor(event)
        assert instance.first_arg == 'test'

    def test_inject_value_from_dependency(self):
        processor = processors.ConstructorInjection()
        processor.container = IocContainer()
        processor.container.add('test', sample_dependency)
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.target['init'] = ['test']
        instance = processor(event)
        assert instance.first_arg == 'test'

    def test_inject_value_from_params(self):
        processor = processors.ConstructorInjection()
        processor.container = IocContainer()
        processor.container.params['test'] = 'blah2'
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.target['init'] = ['test']
        instance = processor(event)
        assert instance.first_arg == 'blah2'

    @raises(TypeError)
    def test_invalid_processor(self):
        processor = SampleProcessor()
        processor('fake event')

    @raises(NameError)
    def test_initialized_invalid_dependency(self):
        processor = processors.ConstructorInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.DoesNotExist')
        processor(event)


class TestSetterInjection(object):

    def test_set_from_dict(self):
        processor = processors.SetterInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.params['definition']['setter'] = {
            'basic_dict_setter': {'kw1': 'one', 'kw2': 'two'}}
        event.target = SampleDependencyAware()
        processor(event)
        assert event.target.kw1 == 'one'
        assert event.target.kw2 == 'two'

    def test_set_from_list(self):
        processor = processors.SetterInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.params['definition']['setter'] = {'basic_list_setter': ['arg']}
        event.target = SampleDependencyAware()
        processor(event)
        assert event.target.arg == 'arg'

    def test_set_from_str(self):
        processor = processors.SetterInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.params['definition']['setter'] = {'basic_setter': 'arg'}
        event.target = SampleDependencyAware()
        processor(event)
        assert event.target.value == 'arg'


class TestAttributeInjection(object):

    def test_inject_property(self):
        processor = processors.AttributeInjection()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.params['definition']['property'] = {
            'basic_property': 'test value'}
        event.target = SampleDependencyAware()
        processor(event)
        assert event.target.basic_property == 'test value'


class TestContainerAwareInjection(object):

    def test_inject_container(self):
        container = IocContainer()
        processor = processors.ContainerAware()
        processor.container = container
        event = sample_event('tests.watson.di.support.SampleDependencyAware')
        event.target = SampleDependencyAware()
        processor(event)
        assert event.target.container == container
