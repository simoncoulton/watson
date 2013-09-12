# -*- coding: utf-8 -*-
from datetime import datetime
import re
from watson.filters import abc
from watson.html.entities import encode


class Trim(abc.Filter):

    """Strips whitespace from value.
    """

    def __call__(self, value):
        """Executes the filter.

        Returns:
            The original value, but whitespace has been removed.
        """
        if not value:
            return value
        return str(value).strip() if isinstance(value, str) else value


class Upper(abc.Filter):

    """Converts all characters to uppercase.

    Usage:
        filter = Upper()
        filter('abcd')  # ABCD
    """

    def __call__(self, value):
        return str(value).upper()


class Lower(abc.Filter):

    """Converts all characters to lowercase.

    Usage:
        filter = Lower()
        filter('ABCD')  # abcd
    """

    def __call__(self, value):
        return str(value).lower()


class RegEx(abc.Filter):

    """Uses regular expressions to replace values.

    Usage:
        filter = RegEx('ing', replacement='ed')
        filter('Stopping')  # Stopped
    """

    def __init__(self, regex, replacement='', flags=0):
        """Initializes the filter.

        Args:
            string|regex regex: The pattern to match.
            string replacement: The value to be used in the replacement.
            int flags: The regex flags.
        """
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.replacement = replacement

    def __call__(self, value):
        """Executes the filter.

        Returns:
            The value with replaced contents.
        """
        return re.sub(self.regex, self.replacement, value)


class Numbers(RegEx):

    """Strips all characters except for numbers.

    Usage:
        filter = Numbers()
        filter('abcd1234')  # 1234
    """

    def __init__(self, regex='[^0-9]', replacement='', flags=0):
        super(Numbers, self).__init__(regex, replacement, flags)


class StripTags(RegEx):

    """Strips all html tags.

    Thanks to django for the regex used below.

    Usage:
        filter = StripTags()
        filter('test<div>blah</div>')  # testblah
    """

    def __init__(
        self, regex=r'</?\S([^=]*=(\s*"[^"]*"|\s*\'[^\']*\'|\S*)|[^>])*?>', flags=re.IGNORECASE):
        super(StripTags, self).__init__(regex, '', flags)


class HtmlEntities(abc.Filter):

    """Encodes all html entities.

    Usage:
        filter = HtmlEntities()
        filter('<div>test</div>')  # &lt;div&gt;test&lt;/div&gt;
    """

    def __call__(self, value):
        return encode(str(value))


class Date(abc.Filter):

    """Formats a string representation of a date to a particular format.

    Usage:
        filter = Date()
        filter('2013-09-12')  # datetime object for that date
    """

    def __init__(self, format='%Y-%m-%d'):
        """Initializes the filter.

        Args:
            string format: The date format to make.
        """
        self.format = format

    def __call__(self, value):
        print(value, self.format)
        if value:
            return datetime.strptime(value, self.format)
        return value
