##############################################################################################################
# Name        : my_profiler
# Description : My handy tool for profiling the code
# Version     : 0.0.0
# Created On  : 2019-06-24
# Modified On : 2020-02-04
# Author      : Hamid R. Darabi, Ph.D.
##############################################################################################################

import time
import functools
import pandas as pd


def f_timer(func):
    """The decorator to time a function code"""
    @functools.wraps(func)
    def wrapper_f_timer(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print("Finished {} in {:.6f} secs".format(func.__name__, run_time))
        return result
    return wrapper_f_timer


class MyTimer():
    def __init__(self, name='', verbose=False):
        self.name = name
        self.verbose = verbose
        self.start = time.time()
        self.last_read = self.start
        self.result = {}

    def elapsed(self, last=False):
        if not last:
            _elapsed = time.time() - self.last_read
            self.last_read = time.time()
            return _elapsed
        return time.time() - self.start

    def checkpoint(self, name, last=False):
        _elapsed = self.elapsed(last)
        if self.verbose:
            print('{timer} {checkpoint} took {elapsed} seconds'.format(
                timer=self.name,
                checkpoint=name,
                elapsed=_elapsed,
            ).strip())
        if name in self.result.keys():
            count, total_time = self.result[name]
            count += 1
            total_time += _elapsed
            self.result[name] = count, total_time
        else:
            self.result[name] = 1, _elapsed

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('total time', last=True)
        self.result = pd.DataFrame(self.result).T
        self.result.columns = ['n_calls', 'tot_time']
        self.result['avg_time'] = self.result['tot_time'] / self.result['n_calls']
        print(self.result)

if __name__ == '__main__':
    def test_function():
        time.sleep(1)

    with MyTimer('test_timer', verbose=True) as t:
        t.checkpoint('task_one')
        test_function()

    @f_timer
    def test_function_two():
        time.sleep(2)

    test_function_two()
