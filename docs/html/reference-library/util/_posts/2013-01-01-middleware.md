---
layout: code
tags: [middleware]
title: Middleware
package: watson.util
module: watson.util.middleware
api: [StaticFileMiddleware]
---

### StaticFileMiddleware

> A WSGI compatibile Middleware class that allows content to be retrieved from the directory that the __main__ is called from.

#### Usage

{% highlight python %}
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello World!']

my_app = StaticFileMiddleware(app)
{% endhighlight %}

#### Methods

##### __init__(app, initial_dir=None)

Type | Name | Description
-------- | -------- | -----------
callable | app | The application to serve
string | initial_dir | The initial directory to serve from

##### __call__(environ, start_response)

###### Returns

The content found at the requested url
