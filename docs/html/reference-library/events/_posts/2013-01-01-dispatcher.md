---
layout: code
tags: [events, dispatcher, mvc]
title: Dispatcher
package: watson.events
module: watson.events.dispatcher
---

### EventDispatcher

> Register and trigger events that will be executed by callables.

The EventDispatcher allows user defined events to be specified. Any listener that is triggered will have the event that was triggered passed to it as the first argument. Attributes can be added to the event params (see watson.events.types.Event) which can then be accessed by the listener.

#### Usage

{% highlight python %}
dispatcher = EventDispatcher()
dispatcher.add('MyEvent', lambda x: x.name)
result = dispatcher.trigger(Event('SampleEvent'))
result.first()  # 'SampleEvent'
{% endhighlight %}

#### Properties

##### events

Returns the events registered on the event dispatcher.

#### Methods

##### clear()

Clears all registered events from the event dispatcher.

##### add(event, callback, priority=1, only_once=False)

Add an event listener to the dispatcher.

Adds an event listener to the relevant event listener collection. If a listener is set to once_only, it will be removed when the event is triggered on the EventDispatcher.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | event | The name of the event
callable | callback | A callable function to be triggered
int | priority | The priority of the listener (higher == more important)
boolean | once_only | When triggered, the listener will be removed

###### Returns

ListCollection: A list of listeners attached to the event

##### remove(event, callback=None)

Remove an event listener from the dispatcher.

Removes an event listener from the relevant Listener.
If no callback is specified, all event listeners for that event are removed.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | event | The name of the event
callable | callback | A callable function to be triggered

###### Returns

Listener: A list of listeners attached to the event

##### __contains__(event):

Return whether or not an event is registered with the event dispatcher.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | event | The name of the event

##### has(event, callback=None):

Return whether or not a callback is found for a particular event.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | event | The name of the event
callable | callback | The callback to find

##### trigger(event)

Fire an event and return a list of results from all listeners.

Dispatches an event to all associated listeners and returns a list of results. If the event is stopped (Event.stopped) then the Result returned will only contain the response from the first listener in the stack.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
watson.events.types.Event | event | The event to trigger

###### Returns

Result: A list of all the responses

--------


### EventDispatcherAware

> Provides an interface for event dispatchers to be injected.

#### Properties

##### dispatcher

Retrieve the event dispatcher. If no event dispatcher exists, create a default one.
