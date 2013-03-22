# -*- coding: utf-8 -*-
from watson.stdlib.imports import get_qualified_name


class Event(object):
    """A base event that can be subclassed for use with an EventDispatcher.

    Usage:
        def my_listener(event):
            print(event.params['config'])

        dispatcher.add('MyEvent', my_listener)

        event = Event('MyEvent')
        event.params['config'] = {'some': 'config'}
        dispatcher.trigger(event)
    """
    _name = None
    _params = None
    _stop_propagation = False
    target = None

    @property
    def name(self):
        """The name of the event
        """
        return self._name

    @property
    def params(self):
        """A dictionary of parameters that can be included within an Event.
        """
        if not self._params:
            self._params = {}
        return self._params

    @params.setter
    def params(self, params):
        """Set the parameters for the event.

        Args:
            dict params: data that is to be sent with the event
        """
        if isinstance(params, dict):
            self._params = params
        else:
            raise TypeError('Event params must be a dictionary.')

    def __init__(self, name, target=None, params=None):
        """Initializes the event.

        Initialize the Event based on an event name. The name will be used
        when the event is triggered from the event dispatcher.

        Args:
            string name: the name of the event
            mixed target: the originating target of the event
            dict params: the params associated with the event
        """
        self._name = str(name)
        self.target = target
        if params is not None:
            self.params = params

    @property
    def stopped(self):
        """Return whether or not the event has been stopped.
        """
        return bool(self._stop_propagation)

    def stop_propagation(self):
        """Prevents the event from triggering any more event listeners.

        This should be used within an event listener when you wish to halt
        any further listeners from being triggered.
        """
        self._stop_propagation = True

    def __repr__(self):
        return '<{0} name:{1}>'.format(get_qualified_name(self), self.name)
