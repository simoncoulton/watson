# -*- coding: utf-8 -*-


class ContainerAware(object):
    """An interface for classes that should have a container.

    Primarily used by the IocContainer, any class that subclasses it will
    have the container it was called from automatically injected into it.
    """
    _container = None

    @property
    def container(self):
        """
        Returns:
            The instance of the injected container.
        """
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
