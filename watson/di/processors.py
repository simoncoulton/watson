# -*- coding: utf-8 -*-
from types import FunctionType
from watson.di import ContainerAware
from watson.stdlib.imports import get_qualified_name, load_definition_from_string


class BaseProcessor(ContainerAware):
    def __call__(self, event):
        raise NotImplementedError(
            'The processor <{}> must implement __call__'.format(get_qualified_name(self)))


class ConstructorInjectionProcessor(BaseProcessor):
    def __call__(self, event):
        item = event.target['item']
        raw = item if isinstance(item, FunctionType) else load_definition_from_string(item)
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
    def __call__(self, event):
        item = event.target
        definition = event.params['definition']
        for setter, args in definition.get('setter', {}).items():
            method = getattr(item, setter)
            if isinstance(args, dict):
                args = {arg: get_param_from_container(value, self.container) for arg, value in args.items()}
                method(**args)
            elif isinstance(args, list):
                args = [get_param_from_container(arg, self.container) for arg in args]
                method(*args)
            else:
                method(get_param_from_container(args, self.container))
        return item


class PropertyInjectionProcessor(BaseProcessor):
    def __call__(self, event):
        item = event.target
        for prop, value in event.params['definition'].get('property', {}).items():
            setattr(item, prop, get_param_from_container(value, self.container))
        return item


class ContainerAwareProcessor(BaseProcessor):
    def __call__(self, event):
        item = event.target
        if isinstance(item, ContainerAware):
            item.container = self.container
        return item


def get_param_from_container(param, container):
    if param in container.params:
        param = container.params[param]
    elif param in container.definitions:
        param = container.get(param)
    return param
