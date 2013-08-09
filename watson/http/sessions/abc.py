# -*- coding: utf-8 -*-
import abc
import datetime
from hashlib import sha1
from random import random
from watson.common.contextmanagers import ignored
from watson.common.imports import get_qualified_name


COOKIE_KEY = 'watson.session'


class StorageMixin(dict, metaclass=abc.ABCMeta):

    """The base mixin for all session storage adapters.

    By default, if no id is specified when the session is created a new
    session id will be generated. When a user is logged in, it is good
    practice to regenerate the id of the session id to prevent
    session hijacking.

    If autosave is set to True, then when data is added to the session
    the save() method will be called. If set to False, the developer
    will be required to manually call the save() method themselves.

    To function correctly sessions require that cookies are enabled in
    the users browser.

    Usage:
        session = SessionStorageMethod()
        # where SessionStorageMethod is a valid storage class
        session['key'] = 'some value'
        session['key'] # 'some value'
    """
    timeout = None
    key = None
    autosave = None
    _id = None
    _data = None
    _cookie_params = None

    @property
    def id(self):
        """The id of the session.
        """
        return self._id

    @property
    def data(self):
        """The data associated with the session.
        """
        return self._data

    @property
    def cookie_params(self):
        """The cookie params used when saving the session id as a cookie.
        """
        if not self._cookie_params:
            self._cookie_params = {
                'expires': 0,
                'path': '/',
                'domain': None,
                'secure': False,
                'httponly': True,
                'comment': 'Watson session id'
            }
        return self._cookie_params

    @cookie_params.setter
    def cookie_params(self, value):
        """Set a dict of cookie params to be used when saving the session id
        """
        self.cookie_params.update(value)

    def __init__(self, id=None, timeout=None, autosave=True):
        """
        Args:
            id: the id of the session
            timeout: the expiry time from the current time in seconds
            key: the key used to reference the session id in a cookie
            autosave: save the contents on __setitem__
        """
        self._id = id
        self.timeout = timeout
        self.key = COOKIE_KEY
        self.timeout = timeout or 60
        self.autosave = autosave
        if not id:
            self.regenerate_id()

    def generate_id(self):
        """
        Return:
            A new session id based on a random 24 char string
        """
        return sha1(str(random()).encode('utf-8')).hexdigest()[:24]

    def regenerate_id(self):
        """Regenerate a new id for the session.
        """
        self._id = self.generate_id()

    def load(self):
        """Loads the data from storage into the session. If the session data was
        set to expire before the current time, destroy the session.
        """
        data = self._load() or ({}, None)
        if data[1] is not None and data[1] < datetime.datetime.now():
            self.destroy()
            self._data = {}
        else:
            self._data = data[0]

    def save(self):
        """Save the contents of the session into storage.
        """
        try:
            timeout = int(self.timeout)
            expires = datetime.datetime.now(
            ) + datetime.timedelta(
                seconds=timeout)
            self._save(expires)
        except:
            raise NotImplementedError(
                'Unable to save the contents of the session')

    def destroy(self):
        """Destroy the session data from storage, but leave the actual session
        intact.
        """
        self._destroy()

    def exists(self):
        """Determine whether or not the session exists in storage.

        Return:
            Boolean whether or not the session id exists.
        """
        return self._exists()

    def get(self, key, default=None):
        return self.__getitem__(key, default)

    # Internals

    def __bool__(self):
        return True  # __iter__ breaks this :(

    def __setitem__(self, key, value):
        if not self.data:
            self._data = {}
        self._data[key] = value
        if self.autosave:
            self.save()

    def __getitem__(self, key, default=None):
        if not self.data:
            self.load()
        return self.data[key] if key in self.data else default

    def __contains__(self, key):
        if not self.data:
            self.load()
        return key in self.data

    def __delitem__(self, key):
        if not self.data:
            self.load()
        with ignored(KeyError):
            del self.data[key]
            if self.autosave:
                self.save()

    def __iter__(self):
        if not self.data:
            self.load()
        for key, value in self.data.items():
            yield (key, value)

    def __repr__(self):
        return '<{0} id:{1}>'.format(get_qualified_name(self), self.id)

    @abc.abstractmethod
    def _load(self):
        raise NotImplementedError('_load must be implemented')

    @abc.abstractmethod
    def _save(self):
        raise NotImplementedError('_save must be implemented')

    @abc.abstractmethod
    def _destroy(self):
        raise NotImplementedError('_destroy must be implemented')

    @abc.abstractmethod
    def _exists(self):
        raise NotImplementedError('_exists must be implemented')
