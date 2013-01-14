# -*- coding: utf-8 -*-
from types import FunctionType
from watson.di.processors import BaseProcessor
from watson.events.dispatcher import EventDispatcherAware
from watson.events.types import Event
from watson.stdlib.datastructures import dict_deep_update
from watson.stdlib.imports import get_qualified_name, load_definition_from_string


PRE_EVENT = 'event.container.pre'
POST_EVENT = 'event.container.post'
DEFAULTS = {
    'params': {},
    'definitions': {},
    'events': {
        PRE_EVENT: [],
        POST_EVENT: [
            'watson.di.processors.InjectProcessor',
            'watson.di.processors.ContainerAwareProcessor'
        ]
    }
}


class IocContainer(EventDispatcherAware):
    config = None
    __instantiated = None

    @property
    def params(self):
        return self.config['params']

    @property
    def definitions(self):
        return self.config['definitions']

    def __init__(self, config=None):
        self.config = dict_deep_update(DEFAULTS, config or {})
        self.__instantiated = {}
        for event, listeners in self.config['events'].items():
            for processor in listeners:
                self.attach_processor(event, load_definition_from_string(processor)())

    def get(self, name):
        definition = self.__find(name)
        if name not in self.__instantiated \
            or definition.get('type', 'singleton').lower() == 'prototype' \
            or isinstance(self.__instantiated.get(name), FunctionType):
            instantiated = self.__create_instance(name, definition)
            self.__instantiated[name] = instantiated
        else:
            instantiated = self.__instantiated[name]
        return instantiated

    def add(self, name, item, type='singleton'):
        definition = self.definitions.get(name, {'item': item})
        self.definitions[name] = definition
        self.__instantiated[name] = item

    def __find(self, name):
        definitions = self.definitions
        if name not in definitions:
            raise KeyError('Dependency {} does not exist'.format(name))
        if 'item' not in definitions[name]:
            raise KeyError('item not specified in dependency definition')
        definition = definitions[name]
        definition['type'] = definition.get('type', 'singleton').lower()
        return definition

    def __create_instance(self, name, definition):
        params = {
            'definition': definition,
            'dependency': name
        }
        pre_process_event = Event(name=PRE_EVENT, target=definition, params=params)
        self.dispatcher.trigger(pre_process_event)
        item = definition['item']
        dependency = item if isinstance(item, FunctionType) else load_definition_from_string(item)
        result = dependency(self) if isinstance(dependency, FunctionType) else dependency()
        post_process_event = Event(name=POST_EVENT, target=dependency, params=params)
        self.dispatcher.trigger(post_process_event)
        return result

    def attach_processor(self, event, processor):
        if not isinstance(processor, BaseProcessor):
            raise TypeError('Processor must be of type {0}'.format(BaseProcessor))
        processor.container = self
        self.dispatcher.add(event, processor)

    def __repr__(self):
        return '<{0}: {1} param(s), ' \
                    '{2} definition(s)>'.format(
                        get_qualified_name(self),
                        len(self.config['params']),
                        len(self.config['definitions']))
