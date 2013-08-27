# -*- coding: utf-8 -*-
import abc
from collections import namedtuple
import importlib
from json import JSONEncoder
import jinja2
import types
from watson.common import datastructures, imports, contextmanagers
from watson.di import ContainerAware
from watson.util import xml


class Model(object):
    format = None
    template = None
    data = None

    def __init__(self, data=None, template=None, format=None):
        self.template = template
        self.data = data
        self.format = format

    def __repr__(self):
        return (
            '<{0} template: {1} format: {2}>'.format(
                imports.get_qualified_name(self),
                self.template,
                self.format)
        )


class BaseRenderer(metaclass=abc.ABCMeta):

    request = None
    response = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def __init__(self, config=None):
        self.config = config or {}

    @abc.abstractmethod
    def __call__(self, view_model):
        # pragma: no cover
        raise NotImplementedError('You must implement __call__')


class Jinja2Renderer(BaseRenderer):
    _env = None

    @property
    def env(self):
        return self._env

    def __init__(self, config=None, application=None):
        super(Jinja2Renderer, self).__init__(config)
        self.register_loaders()
        _types = ('filters', 'globals')
        for _type in _types:
            for module in config[_type]:
                mod = importlib.import_module(module)
                dic = datastructures.module_to_dict(
                    mod, ignore_starts_with='__')
                for name, definition in dic.items():
                    obj = '{0}.{1}'.format(module, name)
                    env_type = getattr(self.env, _type)
                    if isinstance(definition, types.FunctionType):
                        env_type[name] = definition
                    else:
                        env_type[name] = application.container.get(obj)

    def register_loaders(self):
        loaders = [jinja2.FileSystemLoader(path)
                   for path in self.config.get('paths')]
        loaders.append(jinja2.DictLoader({
            'base': '''<!DOCTYPE html>
                <html>
                    <head>
                        {% block head %}
                        <style type="text/css">
                            html, body { font-family: Helvetica, Arial, sans-serif }
                            {% block styles %}{% endblock %}
                        </style>
                        {% endblock %}
                    </head>
                    <body>
                        {% block body %}{% endblock %}
                    </body>
                </html>
            ''',
            'exception_styling': '''
                body {
                    -webkit-font-smoothing: antialiased;
                    margin: 0; padding: 0;
                    font-size: 12px;
                }
                h1, h2 {
                    background: #232e34;
                    color: #fff;
                    margin: 0;
                    padding: 10px;
                    font-weight: normal;
                }
                h1:first-of-type {
                    padding-bottom: 0;
                }
                h2 {
                    color: #3e515a;
                    font-size: 1.1em;
                    padding-top: 0;
                }
                h3 {
                    color: #333;
                    margin-left: 10px;
                }
                p {
                    margin: 0;
                    padding: 10px;
                }
                table {
                    margin: 10px;
                    width: 98%;
                    border-collapse: collapse;
                }
                table th {
                    text-align: left;
                    font-size: 1.1em;
                    padding: 0 6px 6px;
                }
                table td {
                    padding: 6px;
                    vertical-align: top;
                    color: #333;
                }
                .watson-stack-frames > tbody > tr:nth-child(3n+1) {
                    background-color: #fff;
                }
                .watson-stack-frames > tbody > tr {
                    background-color: #f5f5f5;
                }
                .hide {
                    display: none;
                }
                table td {
                    font-family: "Lucida Console", Monaco, monospace;
                }
                dl {
                    margin: 0;
                    padding: 10px;
                }
                dl.watson-info {
                    background: #d9f2fe;
                    color: #1c4d72;
                    border-bottom: 1px solid #9cb3be;
                }
                dl.watson-error {
                    box-shadow: -6px 0 6px rgba(0, 0, 0, 0.05);
                    border-top: 1px solid #00d9ee;
                    border-bottom: 1px solid #00b7df;
                    background: #00bfe3;
                    color: #fff;
                    text-shadow: 0 1px #009fcc;
                    padding-top: 12px;
                }
                dt {
                    font-weight: bold;
                    font-size: 1.1em;
                    float: left;
                    width: 160px;
                    clear: both;
                }
                dd {
                    color: #6087af;
                    margin-bottom: 4px;
                    margin-left: 160px;
                }
                dd table {
                    margin: 0;
                    table-layout: fixed;
                }
                dd table td {
                    font-family: inherit;
                    padding: 2px 0;
                    color: inherit;
                }
                dd table tr > td:first-of-type {
                    width: 200px;
                    overflow: hidden;
                    white-space: nowrap;
                    text-overflow: ellipsis;
                }
                dl.watson-error dd {
                    color: #f6f6f6;
                    padding-top: 2px;
                }
            ''',
            'exception_details': '''
            {% if debug %}
            <h2>{{ message|escape }}</h2>
            <dl class="watson-error">
                <dt>Exception Type:</dt>
                <dd>{{ type }}</dd>
                {% if cause_message %}
                <dt>Exception Message:</dt>
                <dd>{{ cause_message|escape }}</dd>
                {% endif %}
            </dl>
            <dl class="watson-info">
                {% if route_match %}
                <dt>Watson Version:<dt>
                <dd>{{ version }}</dd>
                <dt>Route:</dt>
                <dd>{{ route_match.name|e }}</dd>
                {% endif %}
                <dt>Request:</dt>
                <dd>{{ request.url }}</dd>
                <dt>Method:</dt>
                <dd>{{ request.method }}</dd>
                <dt>Session Id:</dt>
                <dd>{{ request.session.id }}</dd>
                <dt>Headers:</dt>
                <dd>
                    <table>
                    {% for key, value in request.headers|dictsort %}
                        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
                    {% endfor %}
                    </table>
                </dd>
                <dt>Get Vars:</dt>
                <dd>
                    <table>
                    {% for key, value in request.get|dictsort %}
                        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
                    {% else %}
                        -
                    {% endfor %}
                    </table>
                </dd>
                <dt>Post Vars:</dt>
                <dd>
                    <table>
                    {% for key, value in request.post|dictsort %}
                        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
                    {% else %}
                        -
                    {% endfor %}
                    </table>
                </dd>
                <dt>Server:</dt>
                <dd>
                    <table>
                    {% for key, value in request.server|dictsort %}
                        <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
                    {% endfor %}
                    </table>
                </dd>
            </dl>
            <h1>Stack Trace</h1>
            <table class="watson-stack-frames">
            <tr>
                <th>Line</th><th>File</th><th>Function</th><th>Code</th>
            </tr>
            {% for frame in frames %}
            <tr>
                <td>{{ frame.line }}</td>
                <td>{{ frame.file }}</td>
                <td>{{ frame.function }}</td>
                <td>{{ frame.code }}</td>
            </tr>
            {% if frame.vars %}
            {% endif %}
            <tr>
                <td colspan="4" class="hide">
                    <table class="watson-stack-frames-vars">
                        <tr><th>Name</th><th>Value</th></tr>
                        {% for k, v in frame.vars %}
                        <tr>
                            <td>{{ k|e }}</td>
                            <td>{{ v|e }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </td>
            </tr>
            {% endfor %}
            </table>
            {% endif %}
            ''',
            'blank.html': '''{% extends "base" %}
                {% block body %}
                    {{ content }}
                {% endblock %}
            ''',
            'errors/404.html': '''{% extends "base" %}
                {% block styles %}
                    {{ super() }}
                    {% include "exception_styling" %}
                {% endblock %}
                {% block body %}
                    <h1>Not Found</h1>
                    {% include "exception_details" %}
                    {% if not debug %}
                    <p>The requested page cannot be found.</p>
                    {% endif %}
                {% endblock %}
            ''',
            'errors/500.html': '''{% extends "base" %}
                {% block styles %}
                    {{ super() }}
                    {% include "exception_styling" %}
                {% endblock %}
                {% block body %}
                    <h1>Internal Server Error</h1>
                    {% include "exception_details" %}
                    {% if not debug %}
                    <p>A non-recoverable error has occurred and an administrator has been notified.</p>
                    {% endif %}
                {% endblock %}
            '''
        }))
        self._env = jinja2.Environment(loader=jinja2.ChoiceLoader(loaders))

    def __call__(self, view_model):
        template = self._env.get_template(
            '{0}.{1}'.format(view_model.template,
                             self.config['extension']))
        return template.render(view_model.data)


class XmlRenderer(BaseRenderer):

    def __call__(self, view_model):
        _xml = xml.from_dict(view_model.data)
        return xml.to_string(_xml, xml_declaration=True)


class JsonRenderer(BaseRenderer):

    def __call__(self, view_model):
        with contextmanagers.ignored(KeyError):
            del view_model.data['context']
        return JSONEncoder().encode(view_model.data)
