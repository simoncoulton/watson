# -*- coding: utf-8 -*-
from types import FunctionType
from watson.di import ContainerAware
from watson.stdlib.imports import get_qualified_name, load_definition_from_string


class BaseProcessor(ContainerAware):
    """
    The base processor that all other processors should extend.

    When a processor is called from the container the following parameters are
    sent through with the event:
        - definition: The dict definition of the dependency
        - dependency: The name of the dependency
    Depending on the event, a different target will also be sent with the event:
        - watson.di.container.PRE_EVENT: The dict definition of the dependency
        - watson.di.container.POST_EVENT: The initialized dependency
    """
    def __call__(self, event):
        raise NotImplementedError(
            'The processor <{}> must implement __call__'.format(get_qualified_name(self)))


class ConstructorInjectionProcessor(BaseProcessor):
    """
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
        if isinstance(item, FunctionType):
            raw = item
        elif not isinstance(item, str):
            initialized = item
            instantiated = True
        else:
            raw = load_definition_from_string(item)
        if not instantiated:
            args, kwargs = [], {}
            if isinstance(raw, FunctionType):
                kwargs['container'] = self.container
            init = event.target.get('init', {})
            if isinstance(init, dict):
                for kw, args in init.items():
                    kwargs[kw] = get_param_from_container(args, self.container)
            elif isinstance(init, list):
                for arg in init:
                    args.append(get_param_from_container(arg, self.container))
            initialized = raw(*args, **kwargs)
        return initialized


class SetterInjectionProcessor(BaseProcessor):
    """
    Responsible for injecting required values into setter methods.

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
                kwargs = {arg: get_param_from_container(value, self.container) for arg, value in args.items()}
                method(**kwargs)
            elif isinstance(args, list):
                args = [get_param_from_container(arg, self.container) for arg in args]
                method(*args)
            else:
                method(get_param_from_container(args, self.container))
        return item


class PropertyInjectionProcessor(BaseProcessor):
    """
    Responsibile for injecting required values into properties.

    Args:
        watson.events.types.Event event: The event dispatched from the container.

    Returns:
        mixed: The dependency
    """
    def __call__(self, event):
        item = event.target
        for prop, value in event.params['definition'].get('property', {}).items():
            setattr(item, prop, get_param_from_container(value, self.container))
        return item


class ContainerAwareProcessor(BaseProcessor):
    """
    Responsible for injecting the container in any class that extends watson.di.ContainerAware

    Args:
        watson.events.types.Event event: The event dispatched from the container.

    Returns:
        mixed: The dependency
    """
    def __call__(self, event):
        item = event.target
        if isinstance(item, ContainerAware):
            item.container = self.container
        return item


def get_param_from_container(param, container):
    """
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
    return param
