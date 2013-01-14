# -*- coding: utf-8 -*-
from watson.stdlib.imports import get_qualified_name
from watson.di import ContainerAware


class BaseProcessor(ContainerAware):
    def __call__(self, event):
        raise NotImplementedError(
            'The processor <{}> must implement __call__'.format(get_qualified_name(self)))


class InjectProcessor(BaseProcessor):
    def __call__(self, event):
        pass


class ContainerAwareProcessor(BaseProcessor):
    def __call__(self, event):
        pass
