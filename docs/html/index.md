---
layout: default
title: A Python 3 Web Framework
---
<section>

> It's elementary my dear Watson

[![Build Status](https://api.travis-ci.org/simoncoulton/watson.png?branch=master)](https://travis-ci.org/simoncoulton/watson) [![Coverage Status](https://coveralls.io/repos/simoncoulton/watson/badge.png)](https://coveralls.io/r/simoncoulton/watson) [![Pypi](https://pypip.in/v/watson-framework/badge.png)](https://crate.io/packages/watson-framework/)

Watson is an easy to use framework designed to get out of your way and let you code your application rather than spend time wrangling with the framework. It follows the convention over configuration ideal, although the convention can be overriden if required. Out of the box it comes with a standard set of defaults to allow you to get coding straight away!

### Requirements
Watson is designed for Python 3.3 and up.

### Dependencies
Watson currently requires the following modules to work out of box:

* [Jinja2](http://jinja.pocoo.org/docs/) <span class="sub">For view templating</span>

These will be installed automatically if you have installed Watson via pip.

### Optional Dependencies
Some packages within Watson require third party packages to run correctly, these include:

* [Memcached](http://pypi.python.org/pypi/python3-memcached/) <span class="sub">pip package: python3-memcached</span>
* [Redis](https://github.com/andymccurdy/redis-py) <span class="sub">pip package: redis</span>

Notes about these dependencies can be found within the relevant documentation in the [Reference Library]({{ site.baseurl }}/reference-library).

### Testing

Watson can be tested with both py.test and nose (though we recommend py.test).

### Contributing
If you would like to contribute to Watson, please feel free to issue a pull request via Github with the associated tests for your code.
Your name will be added to the AUTHORS file under contributors.
</section>
