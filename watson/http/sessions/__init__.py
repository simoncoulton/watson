# -*- coding: utf-8 -*-
# TODO: MemcachedStorage, DbStorageMixin, MySqlStorage, MongoStorage, RedisStorage
from watson.common.imports import load_definition_from_string
from watson.http.sessions.base import StorageMixin, COOKIE_KEY
from watson.http.sessions.file import FileStorage
from watson.http.sessions.memory import MemoryStorage


__all__ = ['create_session_from_request', 'StorageMixin', 'FileStorage', 'MemoryStorage']


def create_session_from_request(request):
    """
    Creates a new session storage object from a watson.http.messages.Request
    object. If an existing session exists within

    Returns:
        watson.http.sessions.StorageMixin
    """
    storage = load_definition_from_string(request.session_class)
    session_cookie = request.cookies[COOKIE_KEY]
    return storage(id=session_cookie.value) if session_cookie else storage()
