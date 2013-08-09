# -*- coding: utf-8 -*-
import os
import pickle
from tempfile import gettempdir
from watson.common.contextmanagers import ignored
from watson.http.sessions.abc import StorageMixin


class Storage(StorageMixin):

    """A file based storage adapter for session data.

    By default it will store data in the systems temp directory, however this
    can be overriden in the __init__.
    """
    storage = None
    file_prefix = 'session'

    def __init__(self, id=None, timeout=None, autosave=True, storage=None):
        """
        Initialize the File Storage object.

        Args:
            storage: where the files should be stored
        """
        super(Storage, self).__init__(id, timeout, autosave)
        if storage and os.path.exists(storage):
            self.storage = storage
        else:
            self.storage = gettempdir()

    # Internals

    def _exists(self):
        return os.path.exists(self.__file_path())

    def _save(self, expires):
        with open(self.__file_path(), 'wb') as file:
            with ignored(Exception):
                pickle.dump(
                    (self.data,
                     expires),
                    file,
                    pickle.HIGHEST_PROTOCOL)

    def _load(self):
        try:
            with open(self.__file_path(), 'rb') as file:
                with ignored(Exception):
                    return pickle.load(file)
        except:
            return ()

    def _destroy(self):
        with ignored(OSError):
            os.unlink(self.__file_path())

    def __file_path(self):
        return (
            os.path.join(
                self.storage,
                '{0}-{1}'.format(
                    self.file_prefix,
                    self.id))
        )
