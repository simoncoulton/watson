# -*- coding: utf-8 -*-
import abc
from types import FunctionType
from watson.common.imports import get_qualified_name, load_definition_from_string
from watson.common.contextmanagers import ignored
from watson import di


class Base(di.ContainerAware, metaclass=abc.ABCMeta):

    """The base processor that all other processors should extend.

    When a processor is called from the container the following parameters are
    sent through with the event:
        - definition: The dict definition of the dependency
        - dependency: The name of the dependency
    Depending on the event, a different target will also be sent with the event:
        - watson.di.container.PRE_EVENT: The dict definition of the dependency
        - watson.di.container.POST_EVENT: The initialized dependency
    """
    @abc.abstractmethod
    def __call__(self, event):
        raise NotImplementedError(
            'The processor <{}> must implement __call__'.format(get_qualified_name(self)))  # pragma: no cover


class ConstructorInjection(Base):

    """Responsible for initializing the dependency.

    Responsible for initializing the dependency and injecting any required
    values into the constructor.

    Args:
        watson.events.types.Event event: The event dispatched from the container.

    Returns:
        mixed: The dependency
    """

    def __call__(self, event):
        item = event.target['item']
        instantiated = False
        raw = None
        if isinstance(item, FunctionType):
            raw = item
        elif not isinstance(item, str):
            initialized = item
            instantiated = True
        else:
            with ignored(ImportError, AttributeError):
                raw = load_definition_from_string(item)
        if not instantiated:
            if not raw:
                raise NameError(
                    'Cannot initialize dependency {0}, the module may not exist.'.format(item))
            args, kwargs = [], {}
            if isinstance(raw, FunctionType):
                kwargs['container'] = self.container
            init = event.target.get('init', {})
            if isinstance(init, dict):
                for key, val in init.items():
                    kwargs[key] = get_param_from_container(val, self.container)
            elif isinstance(init, list):
                for arg in init:
                    args.append(get_param_from_container(arg, self.container))
            initialized = raw(*args, **kwargs)
        return initialized


class SetterInjection(Base):

    """Responsible for injecting required values into setter methods.

    Args:
        watson.events.types.Event event: The event dispatched from the container.

    Returns:
        mixed: The dependency
    """

    def __call__(self, event):
        item = event.target
        definition = event.params['definition']
        for setter, args in definition.get('setter', {}).items():
            method = getattr(item, setter)
            if isinstance(args, dict):
                kwargs = {arg: get_param_from_container(
                          value,
                          self.container) for arg,
                          value in args.items()}
                method(**kwargs)
            elif isinstance(args, list):
                args = [get_param_from_container(arg, self.container)
                        for arg in args]
                method(*args)
            else:
                method(get_param_from_container(args, self.container))
        return item


class AttributeInjection(Base):

    """Responsible for injecting required values into attributes.

    Args:
        watson.events.types.Event event: The event dispatched from the container.

    Returns:
        mixed: The dependency
    """

    def __call__(self, event):
        item = event.target
        for prop, value in event.params['definition'].get('property', {}).items():
            setattr(
                item,
                prop,
                get_param_from_container(
                    value,
                    self.container))
        return item


class ContainerAware(Base):

    """Injects the container into a dependency.

    Responsible for injecting the container in any class that extends
    watson.di.ContainerAware. The container is then accessible via object.container

    Args:
        watson.events.types.Event event: The event dispatched from the container.

    Returns:
        mixed: The dependency
    """

    def __call__(self, event):
        item = event.target
        if isinstance(item, di.ContainerAware):
            item.container = self.container
        return item


def get_param_from_container(param, container):
    """Internal function used by the container.

    Retrieve a parameter from the container, and determine whether or not that
    parameter is an existing dependency.

    Returns:
        mixed: The dependency (if param name is the same as a dependency), the
               param, or the value of the param.
    """
    if param in container.params:
        param = container.params[param]
    elif param in container.definitions:
        param = container.get(param)
    if isinstance(param, FunctionType):
        param = param(container)
    return param
