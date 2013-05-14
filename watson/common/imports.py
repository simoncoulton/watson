# -*- coding: utf-8 -*-
from importlib import import_module, abc
import sys


def load_definition_from_string(qualified_module):
    """Load a definition based on a fully qualified string.

    Usage:
        definition = load_definition_from_string('watson.http.messages.Request')
        request = definition()

    Return:
        None or the loaded object
    """
    parts = qualified_module.split('.')
    try:
        module = import_module('.'.join(parts[:-1]))
        obj = getattr(module, parts[-1:][0])
        return obj
    except ImportError:
        return None


def get_qualified_name(obj):
    """Retrieve the full module path of an object.

    Usage:
        from watson.http.messages import Request
        request = Request()
        name = get_qualified_name(request) # watson.http.messages.Request
    """
    try:
        name = obj.__qualname__
    except AttributeError:
        try:
            name = obj.__class__.__name__
        except:  # pragma: no cover
            name = obj.__name__  # pragma: no cover
    try:
        module = obj.__module__
        return '{0}.{1}'.format(module, name)
    except:
        return name


class Resolver(abc.Finder, abc.Loader):
    """Allows the ability to inject other modules into an existing package.

    Redirects modules so they can be loaded under the same namespace, which is
    particularly useful for third party extensions.

    Usage:
        # directory structure
        package/
            __init__.py
            module.py
        package_extension.py

        # package/__init__.py
        Resolver('module')

        # package/module.py
        def internal_func(self):
            pass

        # package_extension.py
        def third_party_extension():
            print('called')

        # script.py
        from package.extension import third_party_extension
        third_party_extension()

        >>> python script.py
        # called
    """
    def __init__(self, *modules):
        """Initializes the Resolver.

        Args:
            list modules: A list of string based module names.

        Usage:
            Resolver('watson')
        """
        self.modules = modules
        self.register()

    def find_module(self, fullname, path=None):
        """Determine if the module is to be loaded via the Resolver.

        Args:
            string fullname: The name of the module
            string path: The path to the module
        """
        for module in self.modules:
            if fullname.startswith(module):
                return self
        return None

    def load_module(self, fullname):
        """Loads the module.

        Args:
            string fullname: The name of the module to load
        """
        if fullname not in sys.modules:
            try:
                # first pass attempts to load an existing module, need to drop
                # this loader so that we don't get any recursion.
                self.deregister()
                module = import_module(fullname)
                sys.modules[fullname] = module
                self.register()
            except:
                # second pass attempts to load the 'fake' module.
                module_name = fullname.split('.')
                prefix = module_name.pop(0)
                module_name.insert(0, '{}{}'.format(prefix, '_'))
                actual_name = ''.join(module_name)
                import_module(actual_name)
                sys.modules[fullname] = sys.modules[actual_name]
                sys.modules[fullname].__original_name__ = fullname
                del sys.modules[actual_name]
        return sys.modules[fullname]

    def module_repr(self, module):
        """Retrieve the module repr of a particular module.

        Args:
            string module: The name of the module
        """
        return "<module '{}' from '{}' aliased by '{}'>'".format(module.__name__,
                                                                 module.__file__,
                                                                 module.__original_name__)

    def register(self):
        """Register the resolver.
        """
        sys.meta_path.append(self)

    def deregister(self):
        """Deregisters the resolver.
        """
        sys.meta_path.remove(self)
