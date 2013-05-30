---
layout: code
tags: [mvc, controllers]
title: Controllers
package: watson.mvc
module: watson.mvc.controllers
api: [ActionController, RestController]
---

### Base

> The interface for controller classes.

----------

### HttpMixin

> A mixin for controllers that can contain http request and response objects.

#### Properties

##### event

The event that was triggered that caused the execution of the controller.

##### request

The HTTP request relating to the controller.

##### response

The HTTP response relating to the controller.

##### flash_messages

Retrieves all the flash messages associated with the controller.

###### Usage

{% highlight python %}
# within controller action
self.flash_messages.add('Some message')
return {
    'flash_messages': self.flash_messages
}

# within view
{% raw %}{% for namespace, message in flash_messages %}
    {{ message }}
{% endfor %}{% endraw %}
{% endhighlight %}

#### Methods

##### url(route_name, params=None)

Converts a route into a url.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | route_name | The name of the route to convert
dict | params | The params to use on the route

###### Returns

The assembled url.

##### redirect(path, params=None, status_code=302, clear=False)

Redirecting will bypass the rendering of the view, and the body of the request will be displayed.

Also supports Post Redirect Get (http://en.wikipedia.org/wiki/Post/Redirect/Get) which can allow post variables to accessed from a GET resource after a redirect (to repopulate form fields for example).

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | path | The URL or route name to redirect to
dict | params | The params to send to the route
int | status_code | The status code to use for the redirect
bool | clear | Whether or not the session data should be cleared

###### Returns

A watson.http.messages.Response object.

{% highlight python %}
class Public(controllers.Rest):
    def GET(self):
        return self.redirect('http://google.com')
{% endhighlight %}

##### redirect_vars()

###### Returns

Returns the post variables from a redirected request.

##### clear_redirect_vars()

Clears the redirected variables.

---------

### Action

> A controller thats methods can be accessed with an _action suffix.

{% highlight python %}
class MyController(controllers.Action):
    def my_func_action(self):
        return 'something'
{% endhighlight %}

---------

### Rest

> A controller thats methods can be accessed by the request method name.

{% highlight python %}
class MyController(controllers.Rest):
    def GET(self):
        return 'something'
{% endhighlight %}
