# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import watson


with open('README.md') as f:
    readme = f.read()

with open('LICENCE') as f:
    license = f.read()

setup(
    name='Watson',
    version=watson.__version__,
    description='An easy to use Python 3 framework for creating web applications.',
    long_description=readme,
    author='Simon Coulton',
    author_email='simon.coulton@gmail.com',
    url='https://github.com/simoncoulton/watson',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
