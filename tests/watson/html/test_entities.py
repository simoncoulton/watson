# -*- coding: utf-8 -*-
from watson.html.entities import encode, decode


class TestEncode(object):

    def test_html_chars(self):
        string = '<div><p>some element</p></div>'
        expected = '&lt;div&gt;&lt;p&gt;some element&lt;/p&gt;&lt;/div&gt;'
        assert encode(string) == expected
        assert decode(expected) == string

    def test_double_quotes(self):
        string = '<div> " </div>'
        expected = '&lt;div&gt; &quot; &lt;/div&gt;'
        assert encode(string) == expected
        assert decode(expected) == string

    def test_escaped_slash(self):
        string = "<div> \' </div>"
        expected = '&lt;div&gt; &#x27; &lt;/div&gt;'
        assert encode(string) == expected
        assert decode(expected) == string
