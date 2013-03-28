# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import pickle
from tempfile import gettempdir
try:
    import memcache
except ImportError:
    pass
from watson.stdlib.imports import get_qualified_name


class BaseStorage(object):
    """Base class for all cache storage classes.

    Cache storage classes are designed to act similar to a dict, however get and
    set methods can be used when a timeout is required on a set, or when a default
    value is to be specified on a get.

    Attributes:
        dict config: The relevant configuration settings for the storage.
    """
    config = None

    def __init__(self, config=None):
        self.config = config or {}

    def __setitem__(self, key, value, timeout=0):
        """See set()
        """
        raise NotImplementedError('__setitem__ must be implemented')

    def __getitem__(self, key, default=None):
        """See get()
        """
        raise NotImplementedError('__getitem__ must be implemented')

    def __delitem__(self, key):
        """Delete a key from the cache.

        Args:
            string key: The key to delete

        Usage:
            del cache['key'] # deletes 'key' from the cache
        """
        raise NotImplementedError('__delitem__ must be implemented')

    def __contains__(self, key):
        """Determine whether or not a key exists in the cache.

        Args:
            string key: The key to find

        Returns:
            True/False depending on if the key exists.

        Usage:
            if 'key' in cache:
                print('exists!')
        """
        raise NotImplementedError('__contains__ must be implemented')

    def flush(self):
        """Clears all items from the cache.
        """
        raise NotImplementedError('flush must be implemented')

    def expired(self, key):
        """Determine if a key has expired or not.

        Args:
            string key: The key to find

        Returns:
            True/False depending on expiration
        """
        raise NotImplementedError('expired must be implemented')

    def __repr__(self):
        return '<{0}>'.format(get_qualified_name(self))

    # Convenience methods

    def set(self, key, value, timeout=0):
        """Sets a key in the cache.

        Args:
            string key: The key to be used as a reference
            mixed value: The value to store in the key
            int timeout: The amount of time in seconds a key is valid for.

        Usage:
            cache['key'] = 'value'
        """
        self.__setitem__(key, value, timeout)

    def get(self, key, default=None):
        """Gets a key from the cache, returns the default if not set.

        Args:
            string key: The key to be retrieved

        Returns:
            The value stored within the cache

        Usage:
            value = cache['key']
        """
        return self.__getitem__(key, default)


class Memory(BaseStorage):
    """A cache storage mechanism for storing items in memory.

    Memory cache storage will maintain the cache while the application is being
    run. This is usually best used in instances when you don't want to keep
    the cached items after the application has finished running.
    """
    def __init__(self):
        self._cache = {}

    def __setitem__(self, key, value, timeout=0):
        expires = datetime.now() + timedelta(seconds=int(timeout)) if timeout else None
        self._cache.__setitem__(key, (value, expires))

    def __getitem__(self, key, default=None):
        if self.expired(key):
            return default
        else:
            value, expires = self._stored(key, default)
            return value

    def __delitem__(self, key):
        self._cache.__delitem__(key)

    def flush(self):
        self._cache.clear()
        return True

    def expired(self, key):
        value, expires = self._stored(key)
        if expires is not None and expires < datetime.now():
            return True
        return False

    def __contains__(self, key):
        return self._cache.__contains__(key)

    def _stored(self, key, default=None):
        (value, expires) = self._cache.get(key, (default, None))
        return value, expires


class File(BaseStorage):
    """A cache storage mechanism for storing items on the local filesystem.

    File cache storage will persist the data to the filesystem in whichever
    directory has been specified in the configuration options. If no
    directory is specified then the system temporary folder will be used.
    """
    def __init__(self, config=None):
        """
        Initializes the cache.

        Args:
            dict config: The config for the cache

        Usage:
            cache = File({'dir': '/tmp', 'prefix': 'my-cache'})
            # all cached items will be saved to /tmp
            # and will be prefixed with my-cache
            cache['key'] = 'value' # /tmp/my-cache-key contains a serialized 'value'
        """
        settings = {'dir': gettempdir(), 'prefix': 'cache'}
        if not config:
            config = {}
        settings.update(config)
        self.config = settings

    def __setitem__(self, key, value, timeout=0):
        expires = datetime.now() + timedelta(seconds=int(timeout)) if timeout else None
        with open(self.__file_path(key), 'wb') as file:
            try:
                pickle.dump((value, expires), file, pickle.HIGHEST_PROTOCOL)
            except:
                pass

    def __getitem__(self, key, default=None):
        if self.expired(key):
            return default
        else:
            value, expires = self._stored(key, default)
            return value

    def __delitem__(self, key):
        try:
            os.unlink(self.__file_path(key))
        except OSError:
            pass

    def expired(self, key):
        value, expires = self._stored(key)
        if expires is not None and expires < datetime.now():
            return True
        return False

    def __contains__(self, key):
        return os.path.exists(self.__file_path(key))

    def flush(self):
        storage_dir = self.config['dir']
        index = len(self.config['prefix']) + 1
        files = [f for f in os.listdir(storage_dir) if self.__is_cache_file(f)]
        for file in files:
            del self[file[index:]]
        return True

    def _stored(self, key, default=None):
        value, expires = default, None
        try:
            with open(self.__file_path(key), 'rb') as file:
                try:
                    (value, expires) = pickle.load(file)
                except:
                    pass
        except:
            pass
        return value, expires

    def __cache_file(self, file):
        storage_dir = self.config['dir']
        return os.path.abspath(os.path.join(storage_dir, file))

    def __is_cache_file(self, file):
        if not file.startswith(self.config['prefix']):
            return False
        return os.path.isfile(self.__cache_file(file))

    def __file_path(self, key):
        return os.path.join(self.config['dir'], '{0}-{1}'.format(self.config['prefix'], key))

    def __repr__(self):
        return '<{0} dir:{1}>'.format(get_qualified_name(self), self.config['dir'])


class Memcached(BaseStorage):
    """A cache storage mechanism for storing items in memcached.

    Memcached cache storage will utilize python3-memcached to maintain the cache
    across multiple servers.
    Python3-memcached documentation can be found at http://pypi.python.org/pypi/python3-memcached/
    """
    client = None

    def __init__(self, config=None):
        """
        Initializes the cache.

        Args:
            dict config: The config for the cache

        Usage:
            cache = Memcached({'servers': ['127.0.0.1:11211', '192.168.100.1:11211']})
        """
        settings = {'servers': ['127.0.0.1:11211']}
        if not config:
            config = {}
        settings.update(config)
        self.config = settings

    def __setitem__(self, key, value, timeout=0):
        self.open()
        self.client.set(key, value, timeout)

    def __getitem__(self, key, default=None):
        self.open()
        value = self.client.get(key)
        if not value:
            return default
        return value

    def __delitem__(self, key):
        self.open()
        return self.client.delete(key)

    def flush(self):
        self.open()
        self.client.flush_all()
        return True

    def open(self):
        if not self.client:
            try:
                self.client = memcache.Client(self.config['servers'])
            except:
                raise ImportError('You must have python3-memcached installed.')

    def close(self):
        self.open()
        self.client.disconnect_all()
        return True

    def __contains__(self, key):
        return True if self.get(key) else False

    def expired(self, key):
        return not key in self

    def __repr__(self):
        return '<{0} servers:{1}>'.format(get_qualified_name(self),
                                          len(self.config['servers']))
