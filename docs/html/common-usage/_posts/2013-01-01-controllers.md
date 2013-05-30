---
layout: default
tags: [controllers]
title: Controllers
area: Common Usage
---

<section>

Watson provides two different types of controllers which are called Action and Rest respectively. Each one has its own uses and there is no one size fits all solution.

### Creating controllers

#### <a id="action"></a>Action controllers

Action controller methods are defined explicitly within the applications route configuration. In the following example, when a request is made to `/` then the `app_name.controllers.Public` controller is initialized, and the `indexAction` method is invoked.

<span class="sub">app_name/config/config.py</span>
{% highlight python %}
routes = {
    'index': {
        'path': '/',
        'defaults': {'controller': 'app_name.controllers.Public', 'action': 'index'}
    },
}
{% endhighlight %}

<span class="sub">app_name/controllers/__init__.py</span>
{% highlight python %}
from watson.mvc import controllers

class Public(controllers.Action):
    def index_action(self):
        pass
{% endhighlight %}

#### <a id="rest"></a>RESTful controllers

RESTful controller methods are based upon the HTTP request method that was made by the user. In the following example, when a request is made to `/` the `app_name.controllers.User` controller is initialized, and the relevant HTTP request method is invoked.

<span class="sub">app_name/config/config.py</span>
{% highlight python %}
routes = {
    'index': {
        'path': '/',
        'defaults': {'controller': 'app_name.controllers.User'}
    },
}
{% endhighlight %}

<span class="sub">app_name/controllers/__init__.py</span>
{% highlight python %}
from watson.mvc import controllers

class User(controllers.Rest):
    def GET(self):
        pass

    def POST(self):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass
{% endhighlight %}

### Common tasks


#### Accessing Request and Response objects

No changes should be made to the request object, and they should be treated as immutable. However any modifications can be made to the response object, as it will be used when the application renders the response to the user.

{% highlight python %}
from watson.mvc import controllers

class Controller(controllers.Rest):
    def GET(self):
        request = self.request  # the watson.http.messages.Request object
        response = self.response  # the
{% endhighlight %}

For more information on request and response objects see the [reference library]({{ site.baseurl }}/reference-library/http/messages.html).


#### Redirecting a request to another route or url

{% highlight python %}
from watson.mvc import controllers

class Controller(controllers.Rest):
    def GET(self):
        self.redirect('/')  # redirect the user to specific url

    def POST(self):
        self.redirect('home')  # redirect the user to a named route
{% endhighlight %}

For more information on the various arguments that can be passed to redirect() see the [reference library]({{ site.baseurl }}/reference-library/mvc/controllers.html).

When a user is redirected, any POST or PUT variables will be saved within the users session to solve the PRG ([Post Redirect Get](http://en.wikipedia.org/wiki/Post/Redirect/Get)) issue. These variables may then be accessed to populate a form for example and are stored within the `redirect_vars` attribute of the controller. They can subsequently be cleared via the `clear_redirect_vars()` method on the controller.


#### Flash messaging

Flash messaging is a way to send messages between requests. For example, a user may submit some form data to be saved, at which point the application would

{% highlight python %}
from watson.mvc import controllers
from app_name import forms

class Controller(controllers.Rest):
    def GET(self):
        return {
            'form': forms.Login(),  # form has a POST method
            'flash_messages': self.flash_messages
        }

    def POST(self):
        form = forms.Login()
        form.data = self.request.post
        if form.is_valid():
            self.flash_messages.add('Successfully logged in', 'info')
        else:
            self.flash_messages.add('Invalid username or password', 'error')
        self.redirect('login')
{% endhighlight %}

{% highlight html %}
<html>
    <head></head>
    <body>{% raw %}
        {% for namespace, message in flash_messages %}
        <div class="{{ namespace }}">{{ message }}</div>
        {% endfor %}
        {{ form.open() }}
        {{ form.username.render_with_label() }}
        {{ form.password.render_with_label() }}
        {{ form.submit }}
        {{ form.close() }}
    {% endraw %}</body>
</html>
{% endhighlight %}

Once flash messages have been iterated over, they are automatically cleared from the flash message container.


#### 404 and other http errors

Raising 404 Not Found errors and other HTTP error codes are simple to do directly from the controller.

{% highlight python %}
from watson.mvc import controllers, exceptions

class Controller(controllers.Rest):
    def GET(self):
        raise exceptions.NotFoundError()
{% endhighlight %}

To raise a custom error code, you can raise an ApplicationError with a message and code specified.

{% highlight python %}
from watson.mvc import controllers, exceptions

class Controller(controllers.Rest):
    def GET(self):
        raise exceptions.ApplicationError('Some horrible error', status_code=418)
{% endhighlight %}
</section>
