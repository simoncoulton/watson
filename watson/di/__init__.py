# -*- coding: utf-8 -*-


class ContainerAware(object):
    _container = None

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
