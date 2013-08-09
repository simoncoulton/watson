# -*- coding: utf-8 -*-
from nose.tools import raises
from watson.events import collections


class TestListenerCollection(object):

    def test_create_listener(self):
        assert repr(collections.Listener()
                    ) == '<watson.events.collections.Listener callbacks:0>'

    def test_add_callback(self):
        listener_collection = collections.Listener()
        listener_collection.add(lambda x: x, priority=1)
        assert repr(
            listener_collection) == '<watson.events.collections.Listener callbacks:1>'

    @raises(TypeError)
    def test_add_invalid_callback(self):
        listener_collection = collections.Listener()
        listener_collection.add('test')

    def test_collection_has_callback(self):
        listener_collection = collections.Listener()
        cb = lambda x: x
        listener_collection.add(cb)
        assert cb in listener_collection

    def test_remove_callback(self):
        listener_collection = collections.Listener()
        cb = lambda x: x
        cb2 = lambda y: y
        listener_collection.add(cb)
        assert len(listener_collection) == 1
        listener_collection.add(cb2)
        listener_collection.remove(cb)
        assert len(listener_collection) == 1

    def test_sort_priority(self):
        listener_collection = collections.Listener()
        cb1 = lambda x: x
        cb2 = lambda y: y
        cb3 = lambda z: z
        listener_collection.add(cb1, priority=10)
        listener_collection.add(cb2, priority=30)
        listener_collection.add(cb3, priority=20)
        listener_collection.sort_priority()
        assert listener_collection[0][0] == cb2
        assert listener_collection[2][0] == cb1
        assert listener_collection[1][0] == cb3


class TestResultCollection(object):

    def test_create_result(self):
        collection = collections.Result()
        collection.append('result')
        assert repr(
            collection) == '<watson.events.collections.Result results:1>'

    def test_first_last(self):
        collection = collections.Result()
        collection.append('first')
        collection.append('middle')
        collection.append('last')
        assert collection.first() == 'first'
        assert collection.last() == 'last'

    def test_first_last_not_exists(self):
        collection = collections.Result()
        assert collection.first() is None
        assert collection.last() is None
