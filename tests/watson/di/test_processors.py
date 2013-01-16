# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.di import ContainerAware
from watson.di.processors import ConstructorInjectionProcessor, BaseProcessor
from watson.di.processors import SetterInjectionProcessor, PropertyInjectionProcessor
from watson.di.processors import ContainerAwareProcessor
from watson.di.container import IocContainer
from watson.events.types import Event


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
        processor = ConstructorInjectionProcessor()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.target['init'] = {'sample': 'test'}
        instance = processor(event)
        assert instance.first_kw == 'test'

    def test_inject_value_list(self):
        processor = ConstructorInjectionProcessor()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.target['init'] = ['test']
        instance = processor(event)
        assert instance.first_arg == 'test'

    def test_inject_value_from_dependency(self):
        processor = ConstructorInjectionProcessor()
        processor.container = IocContainer()
        processor.container.add('test', sample_dependency)
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.target['init'] = ['test']
        instance = processor(event)
        assert instance.first_arg == 'blah'

    def test_inject_value_from_params(self):
        processor = ConstructorInjectionProcessor()
        processor.container = IocContainer()
        processor.container.params['test'] = 'blah2'
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.target['init'] = ['test']
        instance = processor(event)
        assert instance.first_arg == 'blah2'

    @raises(NotImplementedError)
    def test_invalid_processor(self):
        processor = SampleProcessor()
        processor('fake event')


class TestSetterInjection(object):
    def test_set_from_dict(self):
        processor = SetterInjectionProcessor()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.params['definition']['setter'] = {'basic_dict_setter': {'kw1': 'one', 'kw2': 'two'}}
        event.target = SampleDependency()
        processor(event)
        assert event.target.kw1 == 'one'
        assert event.target.kw2 == 'two'

    def test_set_from_list(self):
        processor = SetterInjectionProcessor()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.params['definition']['setter'] = {'basic_list_setter': ['arg']}
        event.target = SampleDependency()
        processor(event)
        assert event.target.arg == 'arg'

    def test_set_from_str(self):
        processor = SetterInjectionProcessor()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.params['definition']['setter'] = {'basic_setter': 'arg'}
        event.target = SampleDependency()
        processor(event)
        assert event.target.value == 'arg'


class TestPropertyInjection(object):
    def test_inject_property(self):
        processor = PropertyInjectionProcessor()
        processor.container = IocContainer()
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.params['definition']['property'] = {'basic_property': 'test value'}
        event.target = SampleDependency()
        processor(event)
        assert event.target.basic_property == 'test value'


class TestContainerAwareInjection(object):
    def test_inject_container(self):
        container = IocContainer()
        processor = ContainerAwareProcessor()
        processor.container = container
        event = sample_event('tests.watson.di.test_processors.SampleDependency')
        event.target = SampleDependency()
        processor(event)
        assert event.target.container == container


class SampleProcessor(BaseProcessor):
    pass


class SampleDependency(ContainerAware):
    first_kw = None
    first_arg = None
    kw1 = None
    kw2 = None
    arg = None
    value = None
    basic_property = None

    def __init__(self, *args, **kwargs):
        self.first_kw = kwargs.get('sample')
        try:
            self.first_arg = args[0]
        except:
            self.first_arg = None

    def basic_dict_setter(self, kw1, kw2):
        self.kw1 = kw1
        self.kw2 = kw2

    def basic_list_setter(self, arg):
        self.arg = arg

    def basic_setter(self, value):
        self.value = value


def sample_dependency(container):
    return 'blah'
