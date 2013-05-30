---
layout: code
tags: [di, dependencyinjection]
title: Processors
package: watson.di
module: watson.di.processors
api: [ConstructorInjectionProcessor, SetterInjectionProcessor, AttributeInjectionProcessor, ContainerAwareProcessor]
---

### ConstructorInjection

> Responsible for initializing the dependency.

Responsible for initializing the dependency and injecting any required values into the constructor.

#### Methods

##### __call__(event)

###### Arguments

Type | Name | Description
-------- | -------- | -----------
watson.events.types.Event | event | The event dispatched from the container.


###### Returns

mixed: The dependency


------


### SetterInjection

> Responsible for injecting required values into setter methods.

#### Methods

##### __call__(event)

###### Arguments

Type | Name | Description
-------- | -------- | -----------
watson.events.types.Event | event | The event dispatched from the container.


###### Returns

mixed: The dependency


------

### AttributeInjection

> Responsibile for injecting required values into attributes.

#### Methods

##### __call__(event)

###### Arguments

Type | Name | Description
-------- | -------- | -----------
watson.events.types.Event | event | The event dispatched from the container.


###### Returns

mixed: The dependency


------

### ContainerAware

> Responsible for injecting the container in any class that extends watson.di.ContainerAware. The container is then accessible via object.container.

#### Methods

##### __call__(event)

###### Arguments

Type | Name | Description
-------- | -------- | -----------
watson.events.types.Event | event | The event dispatched from the container.


###### Returns

mixed: The dependency


------
