# -*- coding: utf-8 -*-
from collections import namedtuple
from watson.stdlib.imports import get_qualified_name

Listener = namedtuple('Listener', 'callback priority only_once')


class ListenerCollection(list):
    """A list of listeners to be used in an EventDispatcher.

    A Listener Collection is a list of callbacks that are to be triggered
    by an event dispatcher. Each item in the list contains the callback, a
    priority, and whether or not the callback should only be triggered once.
    """

    require_sort = False

    def add(self, callback, priority=1, only_once=False):
        """Adds a new callback to the collection.

        Args:
            callable callback: the function to be triggered
            int priority: how important the callback is in relation to others
            bool only_once: the callback should only be fired once and then removed

        Raises:
            TypeError if non-callable is added.
        """
        if not hasattr(callback, '__call__'):
            name = get_qualified_name(callback)
            raise TypeError('Callback {0} must be callable.'.format(name))
        self.append(Listener(callback, int(priority), bool(only_once)))
        self.require_sort = True
        return self

    def remove(self, callback):
        """Removes all callbacks matching `callback` from the collection.

        Args:
            callable callback: the callback to be removed.
        """
        i = len(self) - 1
        while i >= 0:
            if self[i].callback == callback:
                listener = self[i]
                super(ListenerCollection, self).remove(listener)
            i -= 1

    def sort_priority(self):
        """Sort the collection based on the priority of the callbacks.
        """
        if self.require_sort:
            self.sort(key=lambda listener: listener.priority, reverse=True)
            self.require_sort = False

    def __contains__(self, callback):
        return [listener for listener in self if listener.callback == callback]

    def __repr__(self):
        return '<{0} callbacks:{1}>'.format(get_qualified_name(self), len(self))


class ResultCollection(list):
    """A list of responses from a EventDispatcher.trigger call.

    A result collection contains all the resulting output from an event that has
    been triggered from an event dispatcher. It provides some convenience methods
    to deal with the results.
    """

    def first(self, default=None):
        """Return the first result from the list.

        Args:
            mixed default: The value to return if the index doesn't exist

        Returns:
            mixed: The first result
        """
        try:
            return self[0]
        except IndexError:
            return default

    def last(self, default=None):
        """Return the last result from the list.

        Args:
            mixed default: The value to return if the index doesn't exist

        Returns:
            mixed: The first result
        """
        try:
            return self[-1]
        except IndexError:
            return default

    def __repr__(self):
        return '<{0} results:{1}>'.format(get_qualified_name(self), len(self))
