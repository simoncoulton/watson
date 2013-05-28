---
layout: code
tags: [cache]
title: Decorators
package: watson.cache
module: watson.cache.decorators
api: [cache]
---

### cache

> Retrieve a value from the cache

Attempts to retrieve a value from the cache. If the wrapped function
does not have an attribute of container, from which to retrieve the cache type then it will default to cache.storage.Memory.

#### Arguments

Type | Name | Description
-------- | -------- | -----------
callable | func | the function that is being wrapped
int | timeout   | the number of seconds the item should exist in the cache
string | key    | the key to store the data against in the cache, defaults to the qualified name of the decorated function.

#### Returns

The contents of the cache key.

#### Usage

{% highlight python %}
class MyClass(ContainerAware):
    @cache(timeout=3600)
    def expensive_func(self):
        return 'something'

c = MyClass()
c.expensive_func() # something
c.expensive_func() # something - returned from cache
{% endhighlight %}
