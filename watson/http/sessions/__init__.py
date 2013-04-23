# -*- coding: utf-8 -*-
# TODO: MemcachedStorage, DbStorageMixin, MySqlStorage, MongoStorage, RedisStorage
from watson.common.imports import load_definition_from_string
from watson.http.sessions.base import StorageMixin, COOKIE_KEY
from watson.http.sessions.file import FileStorage
from watson.http.sessions.memory import MemoryStorage
from watson.http.sessions.memcache import MemcacheStorage


__all__ = ['StorageMixin', 'FileStorage', 'MemoryStorage', 'MemcacheStorage', 'SessionMixin']


class SessionMixin(object):
    """Provides a mixin for Request objects to utilize sessions.
    """
    _session_class = 'watson.http.sessions.FileStorage'
    _session_options = None
    _session = None

    def define_session(self, _class, options=None):
        self._session_class = str(_class)
        self._session_options = options or {}

    @property
    def session(self):
        if not self._session:
            if not self._session_options:
                self._session_options = {}
            storage = load_definition_from_string(self._session_class)
            session_cookie = self.cookies[COOKIE_KEY]
            self._session = storage(id=session_cookie.value, **self._session_options) if session_cookie else storage(**self._session_options)
        return self._session
