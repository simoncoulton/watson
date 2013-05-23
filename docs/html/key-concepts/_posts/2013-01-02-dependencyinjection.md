---
layout: concept
tags: [dependencyinjection]
title: Dependency Injection
---

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

Watson provides an easy to use IoC (Inversion of Control) container which allows these sorts of dependencies to be managed easily. Lets take a look at how we can use this in our application.

<span class="sub">Manually creating a database connection with SQLAlchemy</span>
{% highlight python %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

some_engine = create_engine('postgresql://scott:tiger@localhost/')
Session = sessionmaker(bind=some_engine)
session = Session()

myobject = MyObject('foo', 'bar')
session.add(myobject)
session.commit()
{% endhighlight %}

<span class="sub">app_name/db.py</span>
{% highlight python %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

def create_session(container, connection_string):
    some_engine = create_engine(connection_string)
    session = Session(bind=some_engine)
    return session
{% endhighlight %}

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



<span class="sub">app_name/controllers/my.py</span>
{% highlight python %}
from watson.mvc import controllers

class My(controllers.Rest):
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