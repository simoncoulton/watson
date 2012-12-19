# -*- coding: utf-8 -*-
from watson.stdlib.imports import get_qualified_name
from .collections import ListenerCollection, ResultCollection
from .types import Event


class EventDispatcher(object):

    _events = None

    @property
    def events(self):
        """
        Returns the events registered on the event dispatcher.
        """
        if not self._events:
            self.clear()
        return self._events

    def clear(self):
        """
        Clears all registered events from the event dispatcher.
        """
        self._events = {}

    def add(self, event, callback, priority=1, only_once=False):
        """
        Adds an event listener to the relevant event listener collection. If
        a listener is set to once_only, it will be removed when the event
        is triggered on the EventDispatcher.

        Args:
            string event: The name of the event
            callable callback: A callable function to be triggered
            int priority: The priority of the listener (higher == more important)
            boolean once_only: When triggered, the listener will be removed

        Returns:
            ListCollection: A list of listeners attached to the event
        """
        event = str(event)
        if event not in self.events:
            self.events[event] = ListenerCollection()
        self.events[event].add(callback, int(priority), bool(only_once))
        return self.events[event]

    def remove(self, event, callback=None):
        """
        Removes an event listener from the relevant ListenerCollection.
        If no callback is specified, all event listeners for that event are
        removed.

        Args:
            string event: The name of the event
            callable callback: A callable function to be triggered

        Returns:
            ListenerCollection: A list of listeners attached to the event
        """
        event = str(event)
        if event not in self or not callback:
            self.events[event] = ListenerCollection()
        if callback:
            self.events[event].remove(callback)
        return self.events[event]

    def __contains__(self, event):
        """
        Return whether or not an event is registered with the event dispatcher.
        """
        return event in self.events

    def has(self, event, callback=None):
        """
        Return whether or not a callback is found for a particular event.
        """
        return callback in self.events[event] if event in self.events else False

    def trigger(self, event):
        """
        Dispatches an event to all associated listeners and returns a
        tuple of results. If the event is stopped (Event.stopped) then the
        ResultCollection returned will only contain the response from the
        first listener in the stack.

        Args:
            watson.events.types.Event event: The event to trigger

        Returns:
            ResultCollection: A list of all the responses
        """
        if not isinstance(event, Event):
            raise TypeError('event must be of type watson.events.type.Event')
        results = ResultCollection()
        event.params['dispatcher'] = self
        if event.name in self.events:
            collection = self.events[event.name]
            collection.sort_priority()
            for (callback, priority, only_once) in collection:
                results.append(callback(event))
                if only_once:
                    collection.remove(callback)
                if event.stopped:
                    break

        return results

    def __repr__(self):
        return '<{0} events:{1}>'.format(get_qualified_name(self), len(self.events))


class EventDispatcherAware(object):
    """
    Provides an interface for event dispatcher's to be injected.
    """
    _dispatcher = None

    @property
    def dispatcher(self):
        """
        Retrieve the event dispatcher. If no event dispatcher exists, create
        a default one.

        Returns:
            An EventDispatcher object
        """
        if not self._dispatcher:
            self.dispatcher = EventDispatcher()
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, dispatcher):
        if not isinstance(dispatcher, EventDispatcher):
            raise TypeError('Type must be of EventDispatcher')
        self._dispatcher = dispatcher
