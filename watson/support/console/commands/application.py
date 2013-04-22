# -*- coding: utf-8 -*-
import optparse
import os
from watson.console import ConsoleError
from watson.console.command import BaseCommand
from watson.di import ContainerAware


class CreateApplication(BaseCommand, ContainerAware):
    name = 'newproject'
    help = 'Creates a new project, defaults to the current working directory.'
    arguments = [
        ('project name', 'The name of the project to create.')
    ]
    options = [
        optparse.make_option('-d', '--dir', help='The directory to create the project in.'),
        optparse.make_option('-o', '--override', action='store_const', help='Override any existing project in the path.', const=1)
    ]

    def execute(self):
        if 'project name' not in self.parsed_args:
            raise ConsoleError('No project name specified')
        name = self.parsed_args['project name']
        if self.parsed_options.dir:
            root = os.path.abspath(self.parsed_options.dir)
        else:
            root = os.path.abspath('./')
        basepath = os.path.join(root, name)
        paths = [
            basepath,
            os.path.join(basepath, 'app'),
            os.path.join(basepath, 'app', 'config'),
            os.path.join(basepath, 'app', 'controllers'),
            os.path.join(basepath, 'app', 'views'),
            os.path.join(basepath, 'app', 'views', 'index'),
            os.path.join(basepath, 'data'),
            os.path.join(basepath, 'data', 'cache'),
            os.path.join(basepath, 'data', 'logs'),
            os.path.join(basepath, 'data', 'uploads'),
            os.path.join(basepath, 'public'),
            os.path.join(basepath, 'public', 'css'),
            os.path.join(basepath, 'public', 'img'),
            os.path.join(basepath, 'public', 'js'),
            os.path.join(basepath, 'tests')
        ]
        files = [
            (os.path.join(basepath, 'app', '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'app.py'), APP_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'config', '__init__.py'), BLANK_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'config', 'prod.py'), PROD_CONFIG_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'config', 'dev.py'), DEV_CONFIG_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'config', 'local.py'), DEV_CONFIG_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'config', 'routes.py'), ROUTES_PY_TEMPLATE),
            (os.path.join(basepath, 'app', 'controllers', '__init__.py'), SAMPLE_CONTROLLER_INIT_TEMPLATE),
            (os.path.join(basepath, 'app', 'controllers', 'index.py'), SAMPLE_CONTROLLER_TEMPLATE),
            (os.path.join(basepath, 'app', 'views', 'index', 'get.html'), SAMPLE_VIEW_TEMPLATE),
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
                    file.write(contents)
            except:
                if not self.parsed_options.override:
                    raise ConsoleError('File {0} already exists.'.format(filename))

        # todo, symlink watson-console.py to console.py in project root


BLANK_PY_TEMPLATE = """# -*- coding: utf-8 -*-
"""

APP_PY_TEMPLATE = """# -*- coding: utf-8 -*-
import os
import sys
import watson
from watson.mvc.applications import HttpApplication
from watson.util.server import make_dev_server
from config import local

application = HttpApplication(local)

if __name__ == '__main__':
    make_dev_server(application, do_reload=True)
"""

ROUTES_PY_TEMPLATE = """# -*- coding: utf-8 -*-
routes = {
    'index': {
        'path': '/',
        'defaults': {'controller': 'controllers.Index'}
    }
}
"""

PROD_CONFIG_PY_TEMPLATE = """# -*- coding: utf-8 -*-
from config.routes import routes


debug = {
    'enabled': False,
    'profiling': {
        'enabled': False
    }
}
"""

DEV_CONFIG_PY_TEMPLATE = """# -*- coding: utf-8 -*-
from config.routes import routes


debug = {
    'enabled': True,
    'profiling': {
        'enabled': True
    }
}

"""

SAMPLE_CONTROLLER_INIT_TEMPLATE = """# -*- coding: utf-8 -*-
from controllers.index import Index


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
    </body>
</html>
"""
