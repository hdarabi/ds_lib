##############################################################################################################
# Name        : my_timer
# Description : My handy tool for profiling the code
# Version     : 0.0.0
# Created On  : 2019-06-24
# Modified On : 2019-06-24
# Author      : Hamid R. Darabi, Ph.D.
##############################################################################################################

import time
import pandas as pd


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
        t.checkpoint('start')
        test_function()
