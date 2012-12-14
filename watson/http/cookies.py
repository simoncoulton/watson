# -*- coding: utf-8 -*-
from http.cookies import SimpleCookie, Morsel


class CookieDict(SimpleCookie):
    """
    A basic extension of the SimpleCookie class from the standard library, but
    designed to work better with wsgi.
    """
    def add(self, name, value='', expires=0, path='/', domain=None, secure=False,
            httponly=False, comment=None):
        """
        Convenience method to add cookies to the dict.

        Args:
            name: the name of the cookie
            value: the value of the cookie
            expires: the expiration date for the cookie in seconds
            path: the path in which the cookie is valid
            domain: the domain in which the cookie is valid
            secure: only send cookies over https
            httponly: only send over http requests, not accessible via JavaScript
            comment: the associated comment with the cookie

        Returns:
            The morsel that was added to the CookieDict
        """
        self[name] = value
        morsel = self[name]
        if expires:
            morsel['expires'] = expires
        if path:
            morsel['path'] = path
        if domain:
            morsel['domain'] = domain
        if comment:
            morsel['comment'] = comment
        if secure:
            morsel['secure'] = True
        if httponly:
            morsel['httponly'] = True

        return morsel

    def delete(self, name):
        """
        Expire a cookie the next time it is sent to the browser.

        Args:
            name: the name of the cookie
        """
        self[name].expire()

    def expire(self):
        """
        Expire all the cookies.
        """
        for name in self:
            self.delete(name)

    def __set(self, key, real_value, coded_value):
        # Override the __set method so that we create TastyMorsel's instead.
        M = self.get(key, TastyMorsel())
        M.set(key, real_value, coded_value)
        dict.__setitem__(self, key, M)
    _BaseCookie__set = __set

    def output(self, attrs=None):
        # Override the output so we don't put Set-Cookie in front of each cookie.
        result = []
        for key, value in sorted(self.items()):
            result.append(value.output(attrs))
        return result

    def __getitem__(self, key, default=None):
        return dict.__getitem__(self, key) if key in self else default

    def __str__(self, attrs=None, sep="\015\012"):
        return sep.join(self.output(attrs))


class TastyMorsel(Morsel):
    def output(self, attrs=None):
        # Remove the default value for the header in the outputted string
        # we only want the Set-Cookie header field in the headers module
        return self.OutputString(attrs)
    __str__ = output

    def expire(self):
        self['expires'] = -1
