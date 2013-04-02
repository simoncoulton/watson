# -*- coding: utf-8 -*-
# Runs an extremely simple web application on the development server
# and auto-reloads on change.
# This can either be run via `python app.py` or through uWSGI.
import os
import sys
try:
    import watson
except:
    sys.path.append(os.path.abspath('../../..'))
from watson.mvc.applications import HttpApplication
from watson.util.server import make_dev_server
from config import local

application = HttpApplication(local)

if __name__ == '__main__':
    make_dev_server(application, do_reload=True)
