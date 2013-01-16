# -*- coding: utf-8 -*-


class ContainerAware(object):
    """
    Provides an interface for classes retrieved from a container to have the
    container injected into them.
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
