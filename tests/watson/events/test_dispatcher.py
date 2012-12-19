# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.events.dispatcher import EventDispatcher, EventDispatcherAware
from watson.events.collections import ListenerCollection
from watson.events.types import Event


class SampleDispatcherAware(EventDispatcherAware):
    pass


class TestEventDispatcher(object):
    def test_create_dispatcher(self):
        dispatcher = EventDispatcher()
        assert dispatcher.__repr__() == '<watson.events.dispatcher.EventDispatcher events:0>'

    def test_add_listener(self):
        dispatcher = EventDispatcher()
        func = lambda x: x
        collection = dispatcher.add('SampleEvent', func)
        assert len(dispatcher.events) == 1
        assert len(dispatcher.events['SampleEvent']) == 1
        assert isinstance(collection, ListenerCollection)

    def test_remove_individual_listener(self):
        dispatcher = EventDispatcher()
        func = lambda x: x
        dispatcher.add('SampleEvent', func)
        assert len(dispatcher.events['SampleEvent']) == 1
        dispatcher.remove('SampleEvent', func)
        assert len(dispatcher.events['SampleEvent']) == 0
        collection = dispatcher.remove('NewEvent')
        assert len(collection) == 0

    def test_remove_all_listeners(self):
        dispatcher = EventDispatcher()
        func = lambda x: x
        dispatcher.add('SampleEvent', func)
        dispatcher.add('SampleEvent', func)
        dispatcher.add('SampleEvent', func)
        assert len(dispatcher.events['SampleEvent']) == 3
        dispatcher.remove('SampleEvent')
        assert len(dispatcher.events['SampleEvent']) == 0

    def test_dispatcher_has_event(self):
        dispatcher = EventDispatcher()
        func = lambda x: x
        dispatcher.add('SampleEvent', func)
        assert 'SampleEvent' in dispatcher
        assert dispatcher.has('SampleEvent', func)

    def test_trigger(self):
        dispatcher = EventDispatcher()
        func = lambda x: x.name
        dispatcher.add('SampleEvent', func)
        result = dispatcher.trigger(Event('SampleEvent'))
        assert result.first() == 'SampleEvent'

    @raises(TypeError)
    def test_trigger_invalid_event(self):
        dispatcher = EventDispatcher()
        dispatcher.trigger('test')

    def test_stopped_propagation(self):
        dispatcher = EventDispatcher()

        def func(event):
            event.stop_propagation()
            return event.name
        func2 = lambda x: x.name
        dispatcher.add('SampleEvent', func)
        dispatcher.add('SampleEvent', func2)
        result = dispatcher.trigger(Event('SampleEvent'))
        assert len(result) == 1

    def test_only_one_execution(self):
        dispatcher = EventDispatcher()
        func = lambda x: x.name
        dispatcher.add('SampleEvent', func, only_once=True)
        result = dispatcher.trigger(Event('SampleEvent'))
        assert len(result) == 1
        result2 = dispatcher.trigger(Event('SampleEvent'))
        assert len(result2) == 0


class TestEventDispatcherAware(object):
    def test_is_aware(self):
        sample = SampleDispatcherAware()
        assert isinstance(sample, EventDispatcherAware)
        assert isinstance(sample.dispatcher, EventDispatcher)

    @raises(TypeError)
    def test_invalid_dispatcher(self):
        sample = SampleDispatcherAware()
        sample.dispatcher = 'test'
