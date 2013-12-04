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

    def find_module(self, module_name, path=None):
        """Determine if the module is to be loaded via the Resolver.

        Args:
            string module_name: The name of the module
            string path: The path to the module
        """
        for module in self.modules:
            if module_name.startswith(module):
                return self
        return None

    def load_module(self, module_name):
        """Loads the module.

        Args:
            string module_name: The name of the module to load
        """
        actual_name = module_name.replace('.', '_', 1)
        if module_name not in sys.modules and actual_name not in sys.modules:
            try:
                import_module(actual_name)
            except:
                raise Exception(
                    'Module {0} does not exist (tried to load "{1}")'.format(
                        module_name,
                        actual_name))
        if actual_name in sys.modules and module_name not in sys.modules:
            sys.modules[module_name] = sys.modules[actual_name]
            sys.modules[module_name].__original_name__ = actual_name
            sys.modules[module_name].__name__ = module_name
            del sys.modules[actual_name]
        return sys.modules[module_name]

    def module_repr(self, module):
        """Retrieve the module repr of a particular module.

        Args:
            string module: The name of the module
        """
        if hasattr(module, '__original_name__'):
            return "<module '{}' from '{}' aliased by '{}'>'".format(module.__original_name__,
                                                                     module.__file__,
                                                                     module.__name__)
        else:
            return "<module '{}' from '{}'>'".format(module.__name__,
                                                     module.__file__)

    def register(self):
        """Register the resolver.
        """
        if self not in sys.meta_path:
            sys.meta_path.append(self)

    def deregister(self):
        """Deregisters the resolver.
        """
        sys.meta_path.remove(self)
