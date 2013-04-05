# -*- coding: utf-8 -*-
from watson.http.sessions.base import StorageMixin


class MemoryStorage(StorageMixin):
    """A ram based storage adapter for session data.
    """
    storage = {}

    def _exists(self):
        return self.id in self.storage

    def _save(self, expires):
        self.storage[self.id] = (self.data, expires)

    def _load(self):
        return self.storage.get(self.id)

    def _destroy(self):
        self.storage.pop(self.id, None)
