# -*- coding: utf-8 -*-
from collections import namedtuple
from json import JSONEncoder
from jinja2 import FileSystemLoader, DictLoader, ChoiceLoader, Environment

Model = namedtuple('Model', 'format template data')


class BaseRenderer(object):
    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def __init__(self, config=None):
        self.config = config or {}

    def __call__(self, view_model):
        raise NotImplementedError('You must implement __call__')


class Jinja2Renderer(BaseRenderer):
    _env = None

    def __init__(self, config=None):
        super(Jinja2Renderer, self).__init__(config)
        loaders = [FileSystemLoader(path) for path in self.config.get('paths')]
        loaders.append(DictLoader({
                'base': '''<!DOCTYPE html>
                    <html>
                        <head>
                            {% block head %}
                            <style>
                                html, body {
                                    font-family: Helvetica, Arial, sans-serif
                                }
                            </style>
                            {% endblock %}
                        </head>
                        <body>
                            {% block body %}{% endblock %}
                        </body>
                    </html>
                ''',
                'blank.html': '''{% extends "base" %}
                    {% block body %}
                        {{ content }}
                    {% endblock %}
                ''',
                'errors/404.html': '''{% extends "base" %}
                    {% block body %}
                        <h1>Not Found</h1>
                        <p>{{ message|escape }}</p>
                        <pre>{{ stack|escape }}</pre>
                    {% endblock %}
                ''',
                'errors/500.html': '''{% extends "base" %}
                    {% block body %}
                        <h1>Internal Server Error</h1>
                        <p>{{ message|escape }}</p>
                        <pre>{{ stack|escape }}</pre>
                    {% endblock %}
                '''
            }))
        self._env = Environment(loader=ChoiceLoader(loaders))

    def __call__(self, view_model):
        template = self._env.get_template('{0}.{1}'.format(view_model.template, self.config['extension']))
        return template.render(view_model.data)


class XmlRenderer(BaseRenderer):
    def __call__(self, view_model):
        return '<xml><![CDATA[@todo dict > xml]]></xml>'


class JsonRenderer(BaseRenderer):
    def __call__(self, view_model):
        return JSONEncoder().encode(view_model.data)
