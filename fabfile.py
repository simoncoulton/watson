# -*- coding: utf-8 -*-
from fabric.api import *

CONFIG = {'PY3K_VIRTUALENV': ''}


@task
def py3k(path='venv/'):
    """Sets the Python 3 virtual env path"""
    CONFIG['PY3K_VIRTUALENV'] = 'source {0}bin/activate && '.format(path)


@task
def test():
    """Run all the tests"""
    with hide('running'):
        local('mkdir -p docs/tests/html')
        local('{0}nosetests --config=nose.cfg'.format(CONFIG['PY3K_VIRTUALENV']))


@task
def clean():
    """Removes all the redundant __pycache__ files"""
    with hide('running'):
        local('rm -rf fabfile.pyc')
        local('rm -rf .coverage')
        local('find . -name "__pycache__" -print0|xargs -0 rm -rf')
