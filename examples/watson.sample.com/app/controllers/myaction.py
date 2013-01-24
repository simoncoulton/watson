# -*- coding: utf-8 -*-
from watson.mvc.controllers import ActionController


class MyAction(ActionController):
    def hello_action(self):
        return {}

    def world_action(self):
        return {}

    def json_world_action(self):
        return {'hello': 'world'}
