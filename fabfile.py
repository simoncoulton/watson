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
        test_runner = None
        cli_args = None
        try:
            import nose
            test_runner = 'nosetests'
            cli_args = '--config=nose.cfg'
        except:
            pass  # nosetests not available
        try:
            import pytest
            test_runner = 'py.test'
            cli_args = '-s --cov-report html --cov watson tests/'
        except:
            pass  # pytest not available
        if test_runner:
            print('Running tests via {0}'.format(test_runner))
            local('{0}{1} {2}'.format(CONFIG['PY3K_VIRTUALENV'], test_runner, cli_args))
        else:
            print('You must install either nose or py.test')


@task
def clean():
    """Removes all the redundant __pycache__ files"""
    with hide('running'):
        local('rm -rf fabfile.pyc')
        local('rm -rf .coverage')
        local('find . -name "__pycache__" -print0|xargs -0 rm -rf')
