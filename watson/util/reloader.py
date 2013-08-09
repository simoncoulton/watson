# -*- coding: utf-8 -*-
# Autoreloading launcher.
# Borrowed from Peter Hunt and the CherryPy project (http://www.cherrypy.org).
# Some taken from Ian Bicking's Paste (http://pythonpaste.org/).
# Sourced from the Django project (http://djangoproject.com)
#
# Portions copyright (c) 2004, CherryPy Team (team@cherrypy.org)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of the CherryPy Team nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
import os
import time
import _thread as thread
from watson.common.contextmanagers import ignored

_mtimes = {}


def code_changed():
    global _mtimes
    filenames = [getattr(m, "__file__", None) for m in sys.modules.values()]
    for filename in filter(None, filenames):
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if not os.path.exists(filename):
            continue
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            return True
    return False


def reloader_thread():
    while True:
        if code_changed():
            sys.exit(3)
        time.sleep(1)


def restart_with_reloader(script_dir=None):
    import __main__
    while True:
        if not script_dir:
            script = os.path.abspath(__main__.__file__)
        else:
            script = os.path.abspath(
                os.path.join(script_dir, __main__.__file__))
        args = [sys.executable, script]
        sys_argv = sys.argv[:]
        if len(sys_argv) > 1:
            sys_argv.pop(0)
            args = args + sys_argv
        new_environ = os.environ.copy()
        new_environ['RUN_MAIN'] = 'true'
        exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
        if exit_code != 3:
            return exit_code


def reloader(main_func, args, kwargs, script_dir=None):
    if os.environ.get('RUN_MAIN') == 'true':
        thread.start_new_thread(main_func, args, kwargs)
        with ignored(KeyboardInterrupt):
            reloader_thread()
    else:
        try:
            exit_code = restart_with_reloader(script_dir)
            if exit_code < 0:
                os.kill(os.getpid(), -exit_code)
            else:
                sys.exit(exit_code)
        except KeyboardInterrupt:
            print('\nTerminated.')


def main(main_func, args=None, kwargs=None, script_dir=None):
    reloader(main_func, args or (), kwargs or {}, script_dir)
