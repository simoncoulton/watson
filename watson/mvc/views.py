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
                'exception_styling': '''
                <style>
                    body {
                        margin: 0; padding: 0;
                        font-size: 12px;
                    }
                    h1, h2 {
                        background: #ebebeb;
                        margin: 0;
                        padding: 10px;
                        text-shadow: 1px 1px rgba(255, 255, 255, 0.4)
                    }
                    h2 {
                        color: #666;
                        padding-top: 0;
                        font-size: 1.2em;
                        border-bottom: 1px solid #ccc;
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
                        border-bottom: 1px solid #9cb3be;
                        border-top: 1px solid #fff;
                        background: #d9f2fe;
                        padding: 10px;
                        color: #1c4d72;
                    }
                    dt {
                        font-weight: bold;
                        font-size: 1.1em;
                        float: left;
                        width: 120px;
                        clear: both;
                    }
                    dd {
                        color: #6087af;
                        margin-bottom: 4px;
                        margin-left: 120px;
                    }
                </style>
                ''',
                'exception_details': '''
                {% if debug %}
                <h2>{{ message|escape }}</h2>
                <dl>
                    <dt>Watson Version:<dt>
                    <dd>{{ version }}</dd>
                    <dt>Exception Type:</dt>
                    <dd>{{ type }}</dd>
                    {% if route_match %}
                    <dt>Route:</dt>
                    <dd>{{ route_match.name|e }}</dd>
                    {% endif %}
                    <dt>Request:</dt>
                    <dd>{{ request.url }}</dd>
                    <dt>Method:</dt>
                    <dd>{{ request.method }}</dd>
                    <dt>Headers:</dt>
                    <dd>{{ request.headers }}</dd>
                    <dt>Get Vars:</dt>
                    <dd>{{ request.get }}</dd>
                    <dt>Post Vars:</dt>
                    <dd>{{ request.post }}</dd>
                    <dt>Server:</dt>
                    <dd>{{ request.server }}</dd>
                    <dt>Session Id:</dt>
                    <dd>{{ request.session.id }}</dd>
                </dl>
                <h1>Stack Trace</h1>
                {% if cause_message %}
                <h3>{{ cause_message|escape }}</h3>
                {% endif %}
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
                    {% block head %}
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
                    {% block head %}
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
        self._env = Environment(loader=ChoiceLoader(loaders))

    def __call__(self, view_model):
        template = self._env.get_template('{0}.{1}'.format(view_model.template, self.config['extension']))
        return template.render(view_model.data)


class XmlRenderer(BaseRenderer):
    def __call__(self, view_model):
        return '<?xml version="1.0"?><xml>To be implemented</xml>'


class JsonRenderer(BaseRenderer):
    def __call__(self, view_model):
        return JSONEncoder().encode(view_model.data)
