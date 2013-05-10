# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
import watson
from watson.common.contextmanagers import ignored


with open('LICENSE') as f:
    license = f.read()

try:
    reqs = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(
    name='watson3',
    version=watson.__version__,
    description='An easy to use Python 3 framework for creating web applications.',
    long_description='''Watson, a Python 3 web framework
"It's elementary my dear Watson"

Watson is an easy to use framework designed to get out of your way and let you code your application rather than wrangle with the framework.

The latest documentation can be found at http://simoncoulton.github.com/watson
''',
    author='Simon Coulton',
    author_email='simon.coulton@gmail.com',
    url='http://simoncoulton.github.com/watson',
    license=license,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.3'
    ],
    scripts=['watson/bin/watson-console.py'],
    include_package_data=True,
    install_requires=reqs,
    platforms=['Python 3', 'Python 3.3'],
    keywords=['watson', 'python3', 'web framework', 'framework', 'wsgi']
)
