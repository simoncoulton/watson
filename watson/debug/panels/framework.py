# -*- coding: utf-8 -*-
import watson
from watson.debug import abc

TEMPLATE = """
<dt>Version:</dt>
<dd>{{ version }}</dd>
<b>Events</b>
<br /> {{ get_current_date() }}
{% for name, event in events.items() %}
<i>{{ name }}</i>
<table>
    <tr>
        <th>Callback</th><th>Priority</th><th>Triggered Once</th>
    </tr>
    {% for callback, priority, only_once in event %}
    <tr>
        <td>{{ callback|get_qualified_name }}</td><td>{{ priority }}</td><td>{{ only_once }}</td>
    </tr>
    {% endfor %}
{% endfor %}
</table>
"""


class Panel(abc.Panel):
    title = 'Framework'

    def render(self):
        return self.renderer.env.from_string(TEMPLATE).render(
            version=watson.__version__,
            events=self.application.dispatcher.events)

    def render_key_stat(self):
        return 'v{0}'.format(watson.__version__)
