# -*- coding: utf-8 -*-
import cProfile
import pstats
from watson.di import ContainerAware
# TODO(simon.coulton@gmail.com) All of this is yet to be implemented


class ApplicationInitListener(ContainerAware):
    """
    A listener that will be triggered on watson.mvc.events.INIT.
    Retrieves an instance of the Profiler from the container and overrides
    the 'run' method.
    """
    def __call__(self, event):
        profiler = self.container.get('profiler')
        profiler.register_class(event.target, 'run')


class Profiler(object):
    """
    Allows a piece of code to be profiled and processes the result of the
    profiling.

    Attributes:
        stats: The returned dict for a profiled piece of code
    """
    config = None
    stats = None

    def __init__(self, config=None):
        self.config = config or {}

    def register_class(self, _class, func):
        """
        Replaces a method on _class with it's own __execute method.
        """
        self.original_func = getattr(_class, func)
        setattr(_class, func, self.__execute)

    def __execute(self, *args, **kwargs):
        self.stats = {}
        if self.config.get('enabled', False):
            return self.profile(self.original_func, *args, **kwargs)
        else:
            return self.original_func(*args, **kwargs)

    def profile(self, func, *args, **kwargs):
        """
        Executes a func and profiles it. Sorts the stats cumulatively by default
        unless it is modified in the configuration.

        Usage:
            def my_func():
                do_something()

            profiler = Profiler()
            profiler.profile(my_func)
        """
        profiler = cProfile.Profile()
        response = profiler.runcall(func, *args, **kwargs)
        p = pstats.Stats(profiler)
        p.sort_stats(self.config.get('sort', 'cumulative'))
        f = '{0:.3f}'
        stats = {
            'function_calls': p.total_calls,
            'primative_calls': p.prim_calls,
            'total_time': f.format(p.total_tt),
            'times': []
        }
        list = p.fcn_list
        if list:
            for func in list[:self.config.get('max_results', 20)]:
                cc, nc, tt, ct, callers = p.stats[func]
                c = str(nc)
                if nc != cc:
                    c = c + '/' + str(cc)
                stats['times'].append({
                    'number_calls': c,
                    'total_time': f.format(tt),
                    'per_call': f.format(tt / nc),
                    'cumulative_time': f.format(ct),
                    'per_call2': f.format(ct / cc),
                    'function_name': func[2],
                    'line': func[1],
                    'file': func[0]
                })
        self.stats = stats
        import pprint
        pprint.pprint(self.stats)
        return response
