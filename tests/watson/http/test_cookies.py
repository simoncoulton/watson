# -*- coding: utf-8 -*-
from watson.http.cookies import CookieDict


class TestCookieDict(object):

    def test_add(self):
        cd = CookieDict()
        cd.add(
            name='test',
            value='something',
            expires=60,
            path='/home',
            domain='test.com',
            secure=True,
            httponly=True,
            comment='Blah')
        cookie = cd['test']
        assert cookie.value == 'something'
        assert cookie['expires'] == 60
        assert cookie['path'] == '/home'
        assert cookie['domain'] == 'test.com'
        assert cookie['secure']
        assert cookie['httponly']

    def test_delete(self):
        cd = CookieDict()
        cd.add('test', 'something')
        cd.delete('test')
        assert cd['test']['expires'] == -1

    def test_expire(self):
        cd = CookieDict()
        cd.add('test', 'something')
        cd.add('blah', 'test')
        cd.expire()
        assert cd['test']['expires'] == -1
        assert cd['blah']['expires'] == -1

    def test_output(self):
        cd = CookieDict()
        cd.add('test', 'something')
        cd.add('blah', 'test')
        assert str(cd) == 'blah=test; Path=/\r\ntest=something; Path=/'
