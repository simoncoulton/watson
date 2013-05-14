# -*- coding: utf-8 -*-
# Support functions, classes
from watson.di import processors, ContainerAware


def sample_dependency(container):
    return 'test'


def sample_dependency_with_args(container, arg):
    return arg


class SampleDependency(object):
    pass


class SampleProcessor(processors.Base):
    pass


class SampleDependencyAware(ContainerAware):
    first_kw = None
    first_arg = None
    kw1 = None
    kw2 = None
    arg = None
    value = None
    basic_property = None

    def __init__(self, *args, **kwargs):
        self.first_kw = kwargs.get('sample')
        try:
            self.first_arg = args[0]
        except:
            self.first_arg = None

    def basic_dict_setter(self, kw1, kw2):
        self.kw1 = kw1
        self.kw2 = kw2

    def basic_list_setter(self, arg):
        self.arg = arg

    def basic_setter(self, value):
        self.value = value
