---
layout: code
tags: [common]
title: Decorators
package: watson.common
module: watson.common.decorators
api: [cached_property]
---

### cached_property(func)

> Allows expensive property calls to be cached.

#### Arguments

Type | Name | Description
-------- | -------- | -----------
callable | func | the function that is being wrapped

#### Usage

{% highlight python %}
class MyClass(object):
    @cached_property
    def expensive_call(self):
        # do something expensive

klass = MyClass()
klass.expensive_call  # initial call is made
klass.expensive_call  # return value is retrieved from an internal cache
{% endhighlight %}
