# -*- coding: utf-8 -*-
# TODO: MemcachedStorage, DbStorageMixin, MySqlStorage, MongoStorage, RedisStorage
from watson.common.imports import load_definition_from_string
from watson.http.sessions.base import StorageMixin, COOKIE_KEY
from watson.http.sessions.file import Storage as File
from watson.http.sessions.memory import Storage as Memory
from watson.http.sessions.memcache import Storage as Memcache


__all__ = ['StorageMixin', 'File', 'Memory', 'Memcache', 'SessionMixin']


class SessionMixin(object):
    """Provides a mixin for Request objects to utilize sessions.
    """
    _session_class = 'watson.http.sessions.File'
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

    def session_to_cookie(self):
        session_cookie = self.cookies[COOKIE_KEY]
        if not session_cookie or (session_cookie and self.session.id != session_cookie.value):
            if self.is_secure():
                self.session.cookie_params['secure'] = True
            self.cookies.add(COOKIE_KEY, value=self.session.id, **self.session.cookie_params)
            self.cookies[COOKIE_KEY] = self.session.id
