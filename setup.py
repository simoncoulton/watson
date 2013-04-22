# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import watson


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='watson3',
    version=watson.__version__,
    description='An easy to use Python 3 framework for creating web applications.',
    long_description=readme,
    author='Simon Coulton',
    author_email='simon.coulton@gmail.com',
    url='https://github.com/simoncoulton/watson',
    license=license,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.3'
    ],
    scripts=['watson/bin/watson-console.py'],
    include_package_data=True,
    install_requires=[
        'jinja2 == 2.6'
    ]
)
