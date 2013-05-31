# -*- coding: utf-8 -*-
import collections
from jinja2 import Template
from watson.common import imports
from watson.mvc import events

TEMPLATE = """<!-- Injected Watson Debug Toolbar -->
<style type="text/css">
.watson-debug-toolbar__container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12px;
    background: #e6e6e6;
    color: #7b7c7e;
    border-top: 1px solid #c3c3c3;
}
.watson-debug-toolbar__buttons {
    background: #f2f2f2;
    padding: 8px;
    border-bottom: 1px solid #c3c3c3;
}
.watson-debug-toolbar__buttons a {
    color: inherit;
    text-decoration: none;
    padding: 4px 8px;
    display: inline-block;
    /*background: #f8f8f8;
    border: 1px solid #e9e8e8;*/
    border-radius: 4px;
}
.watson-debug-toolbar__buttons a span {
    color: #aeabab;
    font-weight: bold;
    padding-left: 8px;
}
.watson-debug-toolbar__buttons a.active {
    background: #dcdcdc;
    border-color: #c4c4c4;
    color: #555;
}
.watson-debug-toolbar__container th {
    text-align: left;
}
.watson-debug-toolbar__container #DebugToolbarToggle {
    display: inline-block;
    height: 16px;
    width: 16px;
    background: #fff;
    text-indent: -9999px;
}
.watson-debug-toolbar__panel {
    height: 200px;
    padding: 10px;
    display: none;
    overflow: scroll;
}
.watson-debug-toolbar__container .watson-debug-toolbar__buttons span {
    display: none;
}
.watson-debug-toolbar__container.collapsed .watson-debug-toolbar__panel {
    display: none;
}
.watson-debug-toolbar__container .watson-debug-toolbar__panel.active {
    display: block;
}
.watson-debug-toolbar__container.collapsed .watson-debug-toolbar__buttons span {
    display: inline-block;
}
table {
    width: 100%;
}
table td {
    font-family: inherit;
}
dt {
    font-weight: bold;
    font-size: 1.1em;
    float: left;
    width: 160px;
    clear: both;
}
dd {
    color: inherit;
    margin-bottom: 4px;
    margin-left: 160px;
}
</style>
<div class="watson-debug-toolbar__container collapsed">
    <div class="watson-debug-toolbar__inner">
        <div class="watson-debug-toolbar__buttons">
            <!--<a href="javascript:;" id="DebugToolbarToggle">Toggle</a>-->
            {% for module, panel in panels|dictsort %}
            <a href="javascript:;" data-panel="{{ panel.title }}">{{ panel.title }} <span class="watson-debug-toolbar__key-stat">{{ panel.render_key_stat() }}</span></a>
            {% endfor %}
        </div>
        {% for module, panel in panels|dictsort %}
        <div class="watson-debug-toolbar__panel" data-panel="{{ panel.title }}">
        {{ panel }}
        </div>
        {% endfor %}
    </div>
</div>
<script type="text/javascript" src="http://code.jquery.com/jquery-2.0.2.min.js"></script>
<script type="text/javascript">
    var toolbar = $('.watson-debug-toolbar__container'), toggle = $('#DebugToolbarToggle'), buttons = toolbar.find('.watson-debug-toolbar__buttons a[id!="DebugToolbarToggle"]'), panels = toolbar.find('.watson-debug-toolbar__panel');
    toggle.on('click', function() {
        toolbar.toggleClass('collapsed');
        if (toolbar.hasClass('collapsed')) {
            panels.removeClass('active');
            buttons.removeClass('active');
        }
    });
    buttons.on('click', function() {
        buttons.removeClass('active');
        var that = $(this);
        that.addClass('active');
        panels.removeClass('active');
        toolbar.find('.watson-debug-toolbar__panel[data-panel="'+that.data('panel')+'"]').addClass('active');
        toolbar.removeClass('collapsed');
    });
</script>
"""


class Toolbar(object):
    config = None
    panels = None
    replace_tag = '</body>'

    def __init__(self, config, application, renderer):
        """Application can be any WSGI callable
        """
        self.application = application
        self.config = config
        self.renderer = renderer
        self.panels = collections.OrderedDict()
        for module, settings in config['panels'].items():
            if settings['enabled']:
                panel = imports.load_definition_from_string(module)(settings, renderer, application)
                panel.register_listeners()
                self.panels[module] = panel

    def register_listeners(self):
        self.application.dispatcher.add(events.RENDER_VIEW, self.render, -1000)

    def render(self, event):
        """Render the toolbar to the browser.
        """
        for module, panel in self.panels.items():
            panel.event = event
        response, view_model = event.params['response'], event.params['view_model']
        if view_model.format == 'html':
            html_body = ''.join((self.renderer.env.from_string(TEMPLATE).render(panels=self.panels), self.replace_tag))
            response.body = response.body.replace(self.replace_tag, html_body)
