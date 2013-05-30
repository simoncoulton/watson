---
layout: code
tags: [di, dependencyinjection]
title: Container
package: watson.di
module: watson.di.container
api: [IocContainer]
---

### IocContainer

> A simple dependency injection container that can store and retrieve dependencies for an application.

The container is configured via a dict containing the following keys:<br />

- **params**: a dict of data that can be injected into a dependency.<br />
        If the value of the key is the same as the name of another dependency then the dependency will be referenced.<br />
- **definitions**: a dict of definitions that are to be loaded by the container.<br />
    Available keys within a definition are:<br />
        - item: The qualified name of a class or function<br />
        - type: singleton (only load the dependency once) or prototype (instantiate and return a new dependency on each request)<br />
        - init: a list or dict of items to be injected into the dependency on instantiation.<br />
        - setter: a list or dict of methods to be called upon instantiation.
        - property:
    Only 'item' is a required key.<br />
- **processors**: a dict of events to be listened for and processors to be called.

#### Attributes

Type | Name | Description
-------- | -------- | -----------
dict | config | A dict containing the definitions, params and processors.
dict | __instantiated | A cache of already instantiated dependencies.

#### Usage

{% highlight python %}
container = IocContainer({
    'params': {
        'db.host': 'localhost'
    },
    'definitions': {
        'database': {
            'item': 'db.adapters.MySQL'
            'init': {
                'host': 'db.host',
                'username': 'simon',
                'password': 'test',
                'db': 'test'
            }
        }
    }
})
db = container.get('database')  # an instance of db.adapters.MySQL
{% endhighlight %}


#### Properties

##### params

Convenience method for retrieving the params.

###### Returns

A dict of params.

##### definitions

Convenience method for retrieving the definitions.

###### Returns

A dict of definitions.

###### Usage

{% highlight python %}
Resolver('watson')
{% endhighlight %}

#### Methods

##### \__init\__(config=None)

Initializes the container and set some default configuration options.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
dict | config | A dict containing the params, definitions and processors.

##### get(name)

Retrieve a dependency from the container.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | name | The name of the dependency to retrieve.

###### Raises

Type | Description
-------- | -------- | -----------
KeyError | If the definition or item within the definition are not specified.

###### Returns

mixed: The dependency

##### add(name, item, type='singleton')

Add a dependency to the container (either already instatiated or not).

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | name | The name used to reference the dependency
mixed | item | The dependency to add (either qualified name or instance)

##### attach_processor(event, processor)

Attaches a processor to the container that will be triggered on a specific
        event.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | event | The name of the event (watson.di.container.POST_EVENT or PRE_EVENT)
watson.di.processors.BaseProcessor | processor | The processor to attach.
