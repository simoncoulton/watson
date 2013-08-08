# -*- coding: utf-8 -*-
from copy import deepcopy
from collections import OrderedDict
from types import ModuleType


def dict_deep_update(d1, d2):
    """Recursively merge two dictionaries.

    Merges two dictionaries together rather than a shallow update().

    Args:
        dict d1: The original dict.
        dict d2: The dict to merge with d1.

    Returns:
        A new dict containing the merged dicts.
    """
    if not isinstance(d2, dict):
        return d2
    result = deepcopy(d1)
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_deep_update(result[k], v)
        elif k in result and isinstance(result[k], (list, tuple)) and isinstance(v, (list, tuple)):
            result[k] = result[k] + v
        else:
            result[k] = deepcopy(v)
    return result


def module_to_dict(module, ignore_starts_with=''):
    """Load the contents of a module into a dict.

    Usage:
        # my_module.py contents:
        # variable = 'value'
        import my_module
        a_dict = module_to_dict(my_module)
        a_dict['variable']

    Args:
        string ignore_starts_with: Ignore all module keys that begin with
        this value.

    Return:
        dict
    """
    new_dict = {}
    for k in dir(module):
        item = getattr(module, k)
        if not isinstance(item, ModuleType) and not k.startswith(ignore_starts_with):
            new_dict[k] = item
    return new_dict


class MultiDict(OrderedDict):
    """A dictionary type that can contain multiple items for a single key.

    Dictionary type that will create a list of values if more than one item is
    set for that particular key.

    Usage:
        multi_dict = MultiDict()
        multi_dict['one'] = 1
        multi_dict['one'] = 'itchi'
        print(multi_dict)  # {'one': [1, 'itchi']}
    """

    def set(self, key, value, replace=False):
        """Add a new item to the dictionary.

        Set the key to value on the dictionary, converting the existing value
        to a list if it is a string, otherwise append the value.

        Usage:
            multi_dict = MultiDict()
            multi_dict.set('item', 'value')  # or multi_dict['item'] = 'value'

        Args:
            mixed key: The key used to the store the value.
            mixed value: The value to store.
            boolean replace: Whether or not the value should be replaced.
        """
        self.__setitem__(key, value, replace)

    def __setitem__(self, key, value, replace=False):
        # See MultiDict.set for more information.
        if key in self and not replace:
            if not isinstance(self[key], list):
                existing = [self[key]]
            else:
                existing = self[key]
            existing.append(value)
            new_value = existing
        else:
            new_value = value

        super(MultiDict, self).__setitem__(key, new_value)

    def __getitem__(self, key, default=None):
        return self.get(key, default)


class ImmutableMixin:
    _mutable = True

    def _is_immutable(self):
        if not self._mutable:
            raise TypeError('{0} is immutable'.format(self.__class__.__name__))

    def make_immutable(self):
        self._mutable = False


class ImmutableDict(dict, ImmutableMixin):
    """Creates an immutable dict.

    While not truly immutable (_mutable can be changed), it works effectively.
    """
    def __init__(self, *args):
        super(ImmutableDict, self).__init__(*args)
        self.make_immutable()

    def __setitem__(self, key, value, replace=False):
        self._is_immutable()  # pragma: no cover
        super(ImmutableDict, self).__setitem__(key, value, replace)  # pragma: no cover

    def __delitem__(self, key):
        self._is_immutable()

    def __copy__(self):
        duplicate = {}
        for key, value in self.items():
            duplicate[key] = value
        return duplicate

    def __deepcopy__(self, clone):
        duplicate = {}
        for key, value in self.items():
            duplicate[deepcopy(key, clone)] = deepcopy(value, clone)
        return duplicate

    def appendlist(self, key, value):
        self._is_immutable()  # pragma: no cover
        super(ImmutableDict, self).appendlist(key, value)  # pragma: no cover

    def clear(self):
        self._is_immutable()
        super(ImmutableDict, self).clear()  # pragma: no cover

    def copy(self):
        return self.__deepcopy__({})

    def pop(self, key, *args):
        self._is_immutable()  # pragma: no cover
        return super(ImmutableDict, self).pop(key, *args)  # pragma: no cover

    def popitem(self):
        self._is_immutable()  # pragma: no cover
        return super(ImmutableDict, self).popitem()  # pragma: no cover

    def setdefault(self, key, default=None):
        self._is_immutable()  # pragma: no cover
        return super(ImmutableDict, self).setdefault(key, default)  # pragma: no cover

    def update(self, *args):
        self._is_immutable()  # pragma: no cover
        super(ImmutableDict, self).update(*args)  # pragma: no cover


class ImmutableMultiDict(MultiDict, ImmutableMixin):
    """Creates an immuatable MultiDict.
    """
    def __init__(self, *args):
        super(ImmutableMultiDict, self).__init__(*args)
        self.make_immutable()

    def __setitem__(self, key, value, replace=False):
        self._is_immutable()  # pragma: no cover
        super(ImmutableMultiDict, self).__setitem__(key, value, replace)  # pragma: no cover

    def __delitem__(self, key):
        self._is_immutable()  # pragma: no cover

    def __copy__(self):
        duplicate = MultiDict()
        for key, value in self.items():
            duplicate[key] = value
        return duplicate

    def __deepcopy__(self, clone):
        duplicate = MultiDict()
        for key, value in self.items():
            duplicate[deepcopy(key, clone)] = deepcopy(value, clone)
        return duplicate

    def appendlist(self, key, value):
        self._is_immutable()  # pragma: no cover
        super(ImmutableMultiDict, self).appendlist(key, value)  # pragma: no cover

    def clear(self):
        self._is_immutable()  # pragma: no cover
        super(MultiDict, self).clear()  # pragma: no cover

    def copy(self):
        return self.__deepcopy__(MultiDict())

    def pop(self, key, *args):
        self._is_immutable()  # pragma: no cover
        return super(ImmutableMultiDict, self).pop(key, *args)  # pragma: no cover

    def popitem(self):
        self._is_immutable()  # pragma: no cover
        return super(ImmutableMultiDict, self).popitem()  # pragma: no cover

    def setdefault(self, key, default=None):
        self._is_immutable()  # pragma: no cover
        return super(ImmutableMultiDict, self).setdefault(key, default)  # pragma: no cover

    def update(self, *args):
        self._is_immutable()  # pragma: no cover
        super(ImmutableMultiDict, self).update(*args)  # pragma: no cover
