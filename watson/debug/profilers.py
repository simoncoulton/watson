# -*- coding: utf-8 -*-
import cProfile
import pstats
from watson.di import ContainerAware


class ApplicationInitListener(ContainerAware):
    def __call__(self, event):
        profiler = self.container.get('profiler')
        profiler.register_class(event.target, 'run')


class Profiler(ContainerAware):
    config = None
    stats = None

    def __init__(self, config=None):
        self.config = config or {}

    def register_class(self, _class, func):
        self.original_func = getattr(_class, func)
        setattr(_class, func, self.__execute)

    def __execute(self, *args, **kwargs):
        self.stats = {}
        if self.config.get('enabled', False):
            return self.profile(self.original_func, *args, **kwargs)
        else:
            return self.original_func(*args, **kwargs)

    def profile(self, func, *args, **kwargs):
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
        print(stats)
        return response
