---
layout: code
tags: [mvc, lifecycle]
title: Applications
package: watson.mvc
module: watson.mvc.applications
api: [HttpApplication, ConsoleApplication]
---

### Base

> The core application structure for a Watson application.

It makes heavy use of the IocContainer and EventDispatcher classes to handle
the wiring and executing of methods.
The default configuration for Watson applications can be seen at watson.mvc.config.

#### Properties

##### config

The configuration of the application. This can either be a dict, or a python module.

##### container

The applications IocContainer.

If no container has been created, a new container will be created
based on the dependencies within the application configuration.

#### Methods

##### \__init\__(value)

Registers any events that are within the application configuration.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
mixed | config | See the Base.config property.

##### run(*args, **kwargs)

Called on each request.

--------

### Http

> An application structure suitable for use with the WSGI protocol.

#### Usage

{% highlight python %}
application = applications.Http({..})
application(environ, start_response)
{% endhighlight %}

--------

### Console

> An application structure suitable for the command line.

#### Usage

{% highlight python %}
application = applications.Console({...})
application()
{% endhighlight %}
