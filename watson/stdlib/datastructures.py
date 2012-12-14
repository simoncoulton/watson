# -*- coding: utf-8 -*-
from copy import deepcopy
from collections import OrderedDict


def dict_deep_update(d1, d2):
    """
    Recursively merge two dictionaries together rather than a shallow
    update().
    """
    if not isinstance(d2, dict):
        return d2
    result = deepcopy(d1)
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_deep_update(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


class MultiDict(OrderedDict):
    """
    Dictionary type that will create a list of values if more than one item is
    set for that particular key.
    """

    def set(self, key, value, replace=False):
        self.__setitem__(key, value, replace)

    def __setitem__(self, key, value, replace=False):
        """
        Set the key to value on the dictionary, converting the existing value
        to a list if it is a string, otherwise append the value.

        Args:
            mixed key: The key for the item
            mixed value: The value of the item
            boolean replace: Whether or not to replace the key
        """
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
    """
    Creates an immutable dict. While not truly immutable (_mutable can
    be changed), it works effectively.
    """
    def __init__(self, *args):
        super(ImmutableDict, self).__init__(*args)
        self.make_immutable()

    def __setitem__(self, key, value, replace=False):
        self._is_immutable()
        super(ImmutableDict, self).__setitem__(key, value, replace)

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
        self._is_immutable()
        super(ImmutableDict, self).appendlist(key, value)

    def clear(self):
        self._is_immutable()
        super(ImmutableDict, self).clear()

    def copy(self):
        return self.__deepcopy__({})

    def pop(self, key, *args):
        self._is_immutable()
        return super(ImmutableDict, self).pop(key, *args)

    def popitem(self):
        self._is_immutable()
        return super(ImmutableDict, self).popitem()

    def setdefault(self, key, default=None):
        self._is_immutable()
        return super(ImmutableDict, self).setdefault(key, default)

    def update(self, *args):
        self._is_immutable()
        super(ImmutableDict, self).update(*args)


class ImmutableMultiDict(MultiDict, ImmutableMixin):
    def __init__(self, *args):
        super(ImmutableMultiDict, self).__init__(*args)
        self.make_immutable()

    def __setitem__(self, key, value, replace=False):
        self._is_immutable()
        super(ImmutableMultiDict, self).__setitem__(key, value, replace)

    def __delitem__(self, key):
        self._is_immutable()

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
        self._is_immutable()
        super(ImmutableMultiDict, self).appendlist(key, value)

    def clear(self):
        self._is_immutable()
        super(MultiDict, self).clear()

    def copy(self):
        return self.__deepcopy__(MultiDict())

    def pop(self, key, *args):
        self._is_immutable()
        return super(ImmutableMultiDict, self).pop(key, *args)

    def popitem(self):
        self._is_immutable()
        return super(ImmutableMultiDict, self).popitem()

    def setdefault(self, key, default=None):
        self._is_immutable()
        return super(ImmutableMultiDict, self).setdefault(key, default)

    def update(self, *args):
        self._is_immutable()
        super(ImmutableMultiDict, self).update(*args)
