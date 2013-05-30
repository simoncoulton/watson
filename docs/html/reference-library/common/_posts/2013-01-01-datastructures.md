---
layout: code
tags: [common]
title: Data Structures
package: watson.common
module: watson.common.datastructures
api: [MultiDict, ImmutableDict, ImmutableMultiDict]
---

### dict_deep_update(d1, d2)

> Recursively merge two dictionaries.

Merges two dictionaries together rather than a shallow update().

#### Arguments

Type | Name | Description
-------- | -------- | -----------
dict | d1 | The original dict.
dict | d2 | The dict to merge with d1.

#### Returns

A new dict containing the merged dicts.

#### Usage

{% highlight python %}
d1 = {
        'key': 'value',
        'dict': {
            'key': 'value'
        }
    }
d2 = {
        'dict': {
            'key': 'new value'
        }
    }

d3 = dict_deep_update(d1, d2)
# {'key': 'value', 'dict': {'key': 'new value'}}
{% endhighlight %}


-----

### module_to_dict(module, ignore_starts_with='')

> Load the contents of a module into a dict.

#### Arguments

Type | Name | Description
-------- | -------- | -----------
dict | d1 | The original dict.
dict | d2 | The dict to merge with d1.

#### Returns

A new dict containg the module data

#### Usage

{% highlight python %}
# my_module.py contents:
# variable = 'value'
import my_module
a_dict = module_to_dict(my_module)
a_dict['variable']
{% endhighlight %}

------

### MultiDict

> A dictionary type that can contain multiple items for a single key.

Dictionary type that will create a list of values if more than one item is set for that particular key.

#### Usage

{% highlight python %}
multi_dict = MultiDict()
multi_dict['one'] = 1
multi_dict['one'] = 'itchi'
print(multi_dict)  # {'one': [1, 'itchi']}
{% endhighlight %}

#### Methods

##### set(key, value, replace=False)

Add a new item to the dictionary.
Set the key to value on the dictionary, converting the existing value to a list if it is a string, otherwise append the value.

###### Arguments

Type | Name | Description
-------- | -------- | -----------
mixed | key | The key used to the store the value.
mixed | value | The value to store.
boolean | replace | Whether or not the value should be replaced.


###### Usage

{% highlight python %}
multi_dict = MultiDict()
multi_dict.set('item', 'value')  # or multi_dict['item'] = 'value'
{% endhighlight %}

------

### ImmutableDict

> Creates an immutable dict.

While not truly immutable (_mutable can be changed), it works effectively.

------

### ImmutableMultiDict

> Creates an immuatable MultiDict.
