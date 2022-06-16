import numpy as np
from Modules.Module import Module

from parameters import *

class Linear(Module):
    def __init__(self, start, stop, duration):
        self.start, self.stop, self.duration = self._param_to_modules(
            [start, stop, duration]
        )
        self.cur_x = 0

    def get(self, indexes, input):
        b = self.start.get(indexes, input)
        a = (self.stop.get(indexes, input) - self.start.get(indexes, input)) / self.duration.get(indexes, input)
        xs = np.arange(self.cur_x, self.cur_x + SAMPLES_PER_FRAME)/SAMPLING_FREQUENCY
        self.cur_x += SAMPLES_PER_FRAME
        return b + xs * a
