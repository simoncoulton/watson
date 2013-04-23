# -*- coding: utf-8 -*-
import optparse
import os
import stat
import sys
from string import Template
from watson.console import ConsoleError
from watson.console.command import BaseCommand
from watson.common.imports import load_definition_from_string
from watson.di import ContainerAware
from watson.util.server import make_dev_server


class CreateApplication(BaseCommand, ContainerAware):
    name = 'newproject'
    help = 'Creates a new project, defaults to the current working directory.'
    arguments = [
        ('project name', 'The name of the project to create.'),
        ('app name', 'The name of the application to create.')
    ]
    options = [
        optparse.make_option('-d', '--dir', help='The directory to create the project in.'),
        optparse.make_option('-o', '--override', action='store_const', help='Override any existing project in the path.', const=1)
    ]

    def execute(self):
        if 'project name' not in self.parsed_args:
            raise ConsoleError('No project name specified')
        if 'app name' not in self.parsed_args:
            raise ConsoleError('No app name specified')
        project_name = self.parsed_args['project name']
        app_name = self.parsed_args['app name']
        if self.parsed_options.dir:
            root = os.path.abspath(self.parsed_options.dir)
        else:
            root = os.getcwd()
        basepath = os.path.join(root, project_name)
        paths = [
            basepath,
            os.path.join(basepath, app_name),
            os.path.join(basepath, app_name, 'config'),
            os.path.join(basepath, app_name, 'controllers'),
            os.path.join(basepath, app_name, 'views'),
            os.path.join(basepath, app_name, 'views', 'index'),
            os.path.join(basepath, 'data'),
            os.path.join(basepath, 'data', 'cache'),
            os.path.join(basepath, 'data', 'logs'),
            os.path.join(basepath, 'data', 'uploads'),
            os.path.join(basepath, 'public'),
            os.path.join(basepath, 'public', 'css'),
            os.path.join(basepath, 'public', 'img'),
            os.path.join(basepath, 'public', 'js'),
            os.path.join(basepath, 'tests'),
            os.path.join(basepath, 'tests', app_name),
            os.path.join(basepath, 'tests', app_name, 'controllers'),
        ]
        files = [
            (os.path.join(basepath, app_name, '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'app.py'), APP_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'config', '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'config', 'prod.py'), PROD_CONFIG_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'config', 'dev.py'), DEV_CONFIG_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'config', 'local.py'), DEV_CONFIG_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'config', 'routes.py'), ROUTES_PY_TEMPLATE),
            (os.path.join(basepath, app_name, 'controllers', '__init__.py'), SAMPLE_CONTROLLER_INIT_TEMPLATE),
            (os.path.join(basepath, app_name, 'controllers', 'index.py'), SAMPLE_CONTROLLER_TEMPLATE),
            (os.path.join(basepath, app_name, 'views', 'index', 'get.html'), SAMPLE_VIEW_TEMPLATE),
            (os.path.join(basepath, 'tests', '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, 'tests', app_name, '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, 'tests', app_name, 'controllers', '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, 'tests', app_name, 'controllers', 'test_index.py'), SAMPLE_TEST_SUITE),
            (os.path.join(basepath, 'console.py'), CONSOLE_TEMPLATE),
        ]
        for path in paths:
            try:
                os.mkdir(path)
            except:
                if not self.parsed_options.override:
                    raise ConsoleError('Project already exists at {0}'.format(basepath))
        for filename, contents in files:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(Template(contents).safe_substitute(app_name=app_name))
            except:
                if not self.parsed_options.override:
                    raise ConsoleError('File {0} already exists.'.format(filename))
        st = os.stat(files[-1][0])
        os.chmod(files[-1][0], st.st_mode | stat.S_IEXEC)


class RunDevelopmentServer(BaseCommand, ContainerAware):
    name = 'rundev'
    help = 'Runs the development server for the current application.'

    def execute(self):
        from __main__ import APP_MODULE, APP_DIR, SCRIPT_DIR
        app = load_definition_from_string('{0}.app.application'.format(APP_MODULE))
        os.chdir(APP_DIR)
        make_dev_server(app, do_reload=True, script_dir=SCRIPT_DIR)


class RunTests(BaseCommand, ContainerAware):
    name = 'runtests'
    help = 'Runs the unit tests for the project.'

    def execute(self):
        from __main__ import APP_MODULE
        test_runner = None
        cli_args = ''
        sys.argv = [sys.argv.pop(0)]
        try:
            import pytest
            test_runner = 'pytest'
            cli_args = '--cov {0}'.format(APP_MODULE)
        except:
            try:
                import nose
                test_runner = 'nose'
                cli_args = '--cover-package={0}'.format(APP_MODULE)
            except:
                pass
        if test_runner:
            sys.modules[test_runner].main(cli_args.split(' '))


BLANK_PY_TEMPLATE = """# -*- coding: utf-8 -*-
"""

APP_PY_TEMPLATE = """# -*- coding: utf-8 -*-
from watson.mvc.applications import HttpApplication
from ${app_name}.config import local

application = HttpApplication(local)
"""

ROUTES_PY_TEMPLATE = """# -*- coding: utf-8 -*-
routes = {
    'index': {
        'path': '/',
        'defaults': {'controller': '${app_name}.controllers.Index'}
    }
}
"""

PROD_CONFIG_PY_TEMPLATE = """# -*- coding: utf-8 -*-
from ${app_name}.config.routes import routes


debug = {
    'enabled': False,
    'profiling': {
        'enabled': False
    }
}
"""

DEV_CONFIG_PY_TEMPLATE = """# -*- coding: utf-8 -*-
from ${app_name}.config.routes import routes


debug = {
    'enabled': True,
    'profiling': {
        'enabled': True
    }
}

"""

SAMPLE_CONTROLLER_INIT_TEMPLATE = """# -*- coding: utf-8 -*-
from ${app_name}.controllers.index import Index


__all__ = ['Index']
"""

SAMPLE_CONTROLLER_TEMPLATE = """# -*- coding: utf-8 -*-
from watson import __version__
from watson.mvc.controllers import RestController


class Index(RestController):
    def GET(self):
        return 'Welcome to Watson v{0}!'.format(__version__)
"""

SAMPLE_VIEW_TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        <title>Welcome to Watson!</title>
    </head>
    <body>
        <h1>{{ content }}</h1>
        <p>You are now on your way to creating your first application using Watson.</p>
        <p>Read more about Watson in <a href="http://simoncoulton.github.io/watson/">the documentation.</a>
    </body>
</html>
"""

SAMPLE_TEST_SUITE = """# -*- coding: utf-8 -*-
import watson
from ${app_name}.controllers.index import Index


class TestSuiteIndex(object):
    def test_get(self):
        index = Index()
        assert index.GET() == 'Welcome to Watson v{0}!'.format(watson.__version__)
"""

CONSOLE_TEMPLATE = """#!/usr/bin/env python
import os
import sys

SCRIPT_DIR, SCRIPT_FILE = os.path.split(os.path.abspath(__file__))
APP_MODULE = '${app_name}'
APP_DIR = os.path.join(SCRIPT_DIR, '${app_name}')
try:
    import watson
except:
    # sys.stdout.write('You must have Watson installed, please run `pip install watson3`\\n')
    # sys.exit(1)
    sys.path.append('/Volumes/Data/DevRoot/www/watson')

from watson.mvc.applications import ConsoleApplication

if __name__ == '__main__':
    application = ConsoleApplication()
    application()
"""
