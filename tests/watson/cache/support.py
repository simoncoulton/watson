# -*- coding: utf-8 -*-
# Support functions, classes
from watson.cache.decorators import cache
from watson.di.container import IocContainer


class AClass(object):

    @cache
    def run(self):
        return 'test'


class SampleClass(object):

    def __init__(self):
        self.container = IocContainer({
            'definitions': {
                'application.config': {'item': {'cache': {'type': 'watson.cache.storage.Memory'}}}
            }
        })

    @cache(timeout=60, key='some_key')
    def run(self):
        return 'test'

    @cache
    def tada(self):
        return 'test'
