# -*- coding: utf-8 -*-
from watson.di import ContainerAware
from watson.mvc import applications
from watson.debug import Toolbar


class Init(ContainerAware):

    """Attaches itself to the applications INIT event and initializes the toolbar.
    """

    def __call__(self, event):
        app = event.target
        if isinstance(app, applications.Http):
            debug_config = app.config['debug']
            if debug_config['enabled']:
                toolbar = Toolbar(
                    app.config['debug'],
                    app,
                    self.container.get('jinja2_renderer'))
                toolbar.register_listeners()
