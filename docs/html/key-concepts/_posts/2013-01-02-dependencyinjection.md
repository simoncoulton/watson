---
layout: concept
tags: [dependencyinjection]
title: Dependency Injection
---

* [Introduction](#introduction)
* [Example Usage](#example)
* [Configuring the container](#configuring)

### <a id="introduction"></a>Introduction

Dependency injection is a design pattern that allows us to remove hardcoded dependencies from our code, making it easier to maintain and expand upon as an application grows in size.

<span class="sub">A hardcoded dependency</span>
{% highlight python %}
class MyClass(object):
    def __init__(self):
        self.some_dependency = SomeDependency()

my_class = MyClass()
{% endhighlight %}

<span class="sub">Utilizing dependency injection</span>
{% highlight python %}
class MyClass(object):
    def __init__(self, some_dependency):
        self.some_dependency = some_dependency

my_class = MyClass(SomeDependency())
{% endhighlight %}

As you can see above, the latter removes the dependency from the class itself, creating a looser coupling between components of the application.

#### The lifecycle of a dependency

Dependencies within Watson go through two events prior to being retrieved from the container.

- watson.di.container.PRE_EVENT
<span class="sub">Triggered prior to instantiating the dependency</span>
- watson.di.container.POST_EVENT
<span class="sub">Triggered after instantiating the dependency, by prior to being returned</span>

These events are only triggered once per dependency, unless the dependency is defined as a 'prototype', in which case a new instance of the dependency is retrieved on each request.


### <a id="example"></a>Example Usage

Watson provides an easy to use IoC (Inversion of Control) container which allows these sorts of dependencies to be managed easily. Lets take a look at how we might instantiate a database connection without dependency injection (for a more complete example of this, check out [watson-db](https://github.com/simoncoulton/watson-db))

<span class="sub">app_name/db.py</span>
{% highlight python %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

some_engine = create_engine('postgresql://scott:tiger@localhost/')
Session = sessionmaker(bind=some_engine)
session = Session()
{% endhighlight %}

<span class="sub">app_name/controllers/user.py</span>
{% highlight python %}
from watson.mvc import controllers
from app_name import db

class Profile(controllers.Rest):
    def GET(self):
        return {
            'users': db.session.query(User).all()
        }

    def POST(self):
        user = User(name='user1')
        db.session.add(user)
        db.session.commit()
{% endhighlight %}

One thing to note here is that the configuration for the collection is stored within the code itself. While we could abstract this out to another module, there would still be some sort of dependency on retrieving the configuration from that module. We also introduce a hardcoded dependency by requiring the db module.
By using the IocContainer, we can abstract both of these issues out keeping our codebase clean.

#### Using the IocContainer

First we'll create code required to connect to the database, removing any hardcoded configuration details (note this is purely an example).

<span class="sub">app_name/db.py</span>
{% highlight python %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

def create_session(container, connection_string):
    some_engine = create_engine(connection_string)
    return Session(bind=some_engine)
{% endhighlight %}

Next we have to configure the dependency within the applications configuration settings. [Learn more](#configuring) about the ways to configure your depedencies.

<span class="sub">app_name/config/config.py</span>
{% highlight python %}
dependencies = {
    'definitions': {
        'db_read': {
            'item': 'app_name.db.create_session',
            'init': {
                'connection_string': 'postgresql://read:access@localhost/'
            }
        },
        'db_write': {
            'item': 'app_name.db.create_session',
            'init': {
                'connection_string': 'postgresql://write:access@localhost/'
            }
        }
    }
}
{% endhighlight %}

We now have two dependencies defined in the applications configuration settings. One of the additional benefits of using the IoC container is that subsequent requests for a dependency will return an already instantiated instance of the dependency (unless otherwise specified).

Now all that's left is to retrieve the dependency from the container. We can do this by calling container.get(dependency_name). As controllers are retrieved from the container and extend ContainerAware, our container is automatically injected into them.

<span class="sub">app_name/controllers/user.py</span>
{% highlight python %}
from watson.mvc import controllers

class Profile(controllers.Rest):
    def GET(self):
        # we only want to read from a slave for some reason
        db = self.get('db_read')
        return {
            'users': db.query(User).all()
        }

    def POST(self):
        # we only want writes to go to a specific database
        db = self.get('db_write')
        user = User(name='user1')
        db.add(user)
        db.commit()
{% endhighlight %}

We can also take this a step further and remove the container itself as being a hardcoded dependency (db = self.get('db_*')). We do this by adding the controller itself to the dependency definitions, and injecting the dependency either as a property, setter, or through the constructor. We can get access to the container itself (for retrieving dependencies or configurtion) via lambdas, or just by the same name as the definition. Note that you can also omit the 'item' key if you are configuring a controller.

<span class="sub">app_name/config/config.py</span>
{% highlight python %}
dependencies = {
    'definitions': {
        'db_read': {
            'item': 'app_name.db.create_session',
            'init': {
                'connection_string': 'postgresql://read:access@localhost/'
            }
        },
        'db_write': {
            'item': 'app_name.db.create_session',
            'init': {
                'connection_string': 'postgresql://write:access@localhost/'
            }
        },
        'app_name.controllers.user.Profile': {
            'property': {
                'db_read': 'db_read',  # References the db_read definition
                'db_write': 'db_write'
            }
        }
    }
}
{% endhighlight %}

Now we simply modify our controller to suit the new definitions...

<span class="sub">app_name/controllers/user.py</span>
{% highlight python %}
from watson.mvc import controllers

class Profile(controllers.Rest):
    db_read = None
    db_write = None

    def GET(self):
        return {
            'users': self.db_read.query(User).all()
        }

    def POST(self):
        user = User(name='user1')
        self.db_write.add(user)
        self.db_write.commit()
{% endhighlight %}


### <a id="configuring"></a>Configuring the container

The container is defined within your applications configuration under the key 'dependencies' as seen below.

{% highlight python %}
dependencies = {
    'params': {
        'param_name': 'value'
    },
    'definitions': {
        'name': {
            'item': 'package.module.object',
            'type': 'singleton',
            'init': {
                'keyword': 'arg'
            },
            'property': {
                'attribute': 'value'
            },
            'setter': {
                'method_name': {
                    'keyword': 'arg'
                }
            }
        }
    }
}
{% endhighlight %}

Lets break this down into it's different components:

<span class="sub">params</span>
{% highlight python %}
'params': {
    'param_name': 'value'
}
{% endhighlight %}

Params are arguments that can be inserted into dependencies via init, property or setter processors. Any argument that is being used in one of the above processor definitions will be evaluated against the params and replaced with it's value. If a param value has the same name as a dependency, then that dependency itself will be injected.

<span class="sub">An example dependency using params</span>
{% highlight python %}
dependencies = {
    'params': {
        'host': '127.0.0.1'
    },
    'definitions': {
        'db': {
            'item': 'app.db',
            'init': {
                'hostname': 'host'
            }
        }
    }
}
{% endhighlight %}

When the above dependency is retrieved, the 'host' param will be injected into the objects constructor.
