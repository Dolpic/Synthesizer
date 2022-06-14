import numpy as np

from Modules.Module import *
from parameters import *

class Linear(Module):
    def __init__(self, start, stop, duration):
        super().__init__()
        params = [start, stop, duration]
        self._param_to_modules(params)
        self.start = params[0]
        self.stop  = params[1]
        self.duration = params[2]

    def get(self, input):
        times = self._get_next_times(len(input))
        b = self.start.get(input)
        a = (self.stop.get(input) - self.start.get(input)) / self.duration.get(input)
        return b + times * a