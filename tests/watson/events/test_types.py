# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.events.types import Event


class TestEvent(object):

    def test_create_event(self):
        assert repr(Event(name='SampleEvent')
                    ) == '<watson.events.types.Event name:SampleEvent>'

    def test_event_target(self):
        event = Event('SamplEvent', target=self)
        assert event.target == self

    def test_add_remove_params(self):
        event = Event('SampleEvent')
        event.params['test'] = 'test'
        assert event.params['test'] == 'test'
        del event.params['test']
        assert 'test' not in event.params

    @raises(TypeError)
    def test_set_invalid_params(self):
        Event('SampleEvent', params='test')

    def test_set_valid_params(self):
        event = Event('SampleEvent', params={'test': 'test'})
        assert event.params['test'] == 'test'

    def test_stop_propagation(self):
        event = Event('SampleEvent')
        assert event.stopped == False
        event.stop_propagation()
        assert event.stopped
