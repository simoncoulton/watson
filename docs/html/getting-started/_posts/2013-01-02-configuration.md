---
layout: default
tags: [configuration, getting started]
title: Configuration
area: Getting Started
---
<section>

* [Introduction](#introduction)
* [Application Configuration](#application)
* [Extending the Configuration](#extending)


### <a id="introduction"></a>Introduction
While Watson is primarily built with conventions in mind, there are still plenty of configuration options that can be modified to override the default behaviour.

> **Note:** To override values within the default configuration, you only need to replace those values within your own configuration file. The application with automatically merge the defaults with your new options.

### <a id="application"></a>Application Configuration

Configuration for Watson is just a standard python module (and should be familiar to those who have used Django previously). Available keys for configuration are:

* debug
* dependencies
* views
* session
* events

You can see the default configuration that Watson uses within the `watson.mvc.config` module.

#### Debug

Debug is responsible for determining if the application is running in debug mode, and the relevant profiling settings.

<span class="sub">watson.mvc.config</span>
{% highlight python %}
debug = {
    'enabled': False,
    'panels': {
        'watson.debug.panels.request.Panel': {
            'enabled': True
        },
        'watson.debug.panels.application.Panel': {
            'enabled': True
        },
        'watson.debug.panels.profile.Panel': {
            'enabled': True,
            'max_results': 20,
            'sort': 'time',
        },
        'watson.debug.panels.framework.Panel': {
            'enabled': True
        },
    }
}
{% endhighlight %}

#### Dependencies

The configuration of your application will automatically be added to the container, which can then be retrieved via the key `application.config`.

See the dependency injection [key concept](/watson/key-concepts/dependencyinjection.html#configuring) for more information on how to define dependencies and container parameters.

#### Views

Watson utilizes multiple renderers to output the different views that the user may request. Each renderer is retrieved
from the dependency injection container (see above), with the name key being the same as the relevant dependency name.

<span class="sub">watson.mvc.config</span>
{% highlight python %}
views = {
    'default_format': 'html',
    'renderers': {
        'default': {
            'name': 'jinja2_renderer',
            'config': {
                'extension': 'html',
                'paths': [os.path.join(os.getcwd(), 'views')]
            }
        },
        'xml': {'name': 'xml_renderer'},
        'json': {'name': 'json_renderer'}
    },
    'templates': {
        '404': 'errors/404',
        '500': 'errors/500'
    }
}
{% endhighlight %}

The above configuration sets the default renderer to use Jinja2. It also specifies two other renderers, which will output
XML and JSON respectively.
There are also a set of templates defined, which allows you to override templates that will be used. The format of these being 'existing template path': 'new template path' (relative to the views directory).


#### Session

By default Watson will use File for session storage, which stores the contents of each session in their own file
within your systems temporary directory (unless otherwise specified in the config).

<span class="sub">watson.mvc.config</span>
{% highlight python %}
session = {
    'class': 'watson.http.sessions.File',
    'options': {}  # a dict of options for the storage class
}
{% endhighlight %}

See the storage methods that are available for sessions in the [Reference Library](/watson/reference-library/http/sessions.html).


#### Events

Events are the core to the lifecycle of both a request and the initialization of a Watson application. The default configuration sets up 5 events which will be executed at different times of the lifecycle.

<span class="sub">watson.mvc.config</span>
{% highlight python %}
events = {
    events.EXCEPTION: [('app_exception_listener',)],
    events.INIT: [
        ('watson.debug.profilers.ApplicationInitListener', 1, True)
    ],
    events.ROUTE_MATCH: [('watson.mvc.listeners.RouteListener',)],
    events.DISPATCH_EXECUTE: [('app_dispatch_execute_listener',)],
    events.RENDER_VIEW: [('app_render_listener',)],
}
{% endhighlight %}

### <a id="extending"></a>Extending the Configuration

There are times when you may want to allow other developers to get access to your configuration from dependencies retrieved from the
container. This can easily be achieved by the use of lambda functions.

First create the settings you wish to retrieve in your settings:

<span class="sub">app/config/config.py</span>
{% highlight python %}
my_class_config = {
	'a_setting': 'a value'
}
{% endhighlight %}

And then within your dependency definitions you can reference it like this:

<span class="sub">app/config/config.py</span>
{% highlight python %}
dependencies = {
	'definitions': {
		'my_class': {
			'item': 'my.module.Klass',
			'init': [lambda ioc: ioc.get('application.config')['my_class_config']]
		}
	}
}
{% endhighlight %}

When my.module.Klass is initialized, the configuration settings will be passed as the first argument to the `__init__` method.

</section>
