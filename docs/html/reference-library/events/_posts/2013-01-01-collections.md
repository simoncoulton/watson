---
layout: code
tags: [events, collections, dispatcher, mvc]
title: Collections
package: watson.events
module: watson.events.collections
api: [ListenerCollection, ResultCollection]
---

### ListenerDefinition

A named tuple consisting of a callback, priority, and once_only flag.

--------

### Listener

> A list of listeners to be used in an EventDispatcher.

A Listener Collection is a list of callbacks that are to be triggered by an event dispatcher. Each item in the list contains the callback, a priority, and whether or not the callback should only be triggered once.

#### Methods

##### add(callback, priority=1, only_once=False)

Adds a new callback to the collection.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
callable | callback | the function to be triggered
int | priority | how important the callback is in relation to others
bool | only_once | the callback should only be fired once and then removed

###### Raises

TypeError if non-callable is added.

##### remove(callback)

Removes all callbacks matching `callback` from the collection.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
callable | callback | the callback to be removed.

##### sort_priority()

Sort the collection based on the priority of the callbacks.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
callable | callback | the callback to be removed.

##### \__contains\__(callback)

Determine whether or not a callback is in the collection.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
callable | callback | the callback to be removed.

---------

### Result

> A list of responses from a EventDispatcher.trigger call.

A result collection contains all the resulting output from an event that has
been triggered from an event dispatcher. It provides some convenience methods to deal with the results.

#### Methods

##### first(default=None)

Return the first result from the list.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
mixed | default | The value to return if the index doesn't exist

###### Returns

mixed: The first result in the collection

##### last(default=None)

Return the last result from the list.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
mixed | default | The value to return if the index doesn't exist

###### Returns

mixed: The last result in the collection

