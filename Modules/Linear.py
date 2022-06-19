import numpy as np
import parameters

from Modules.Module import Module

"""
Module implementing an linear function.

This module applies a linear function on the given indexes.
The linear function start at a given value and reaches an end 
value after a given time in seconds.

Parameters :
start : starting value of the function
stop : end value of the function
duration : duration in seconds to go from the start value to the end value

"""

class Linear(Module):
    def __init__(self, start, stop, duration):
        self.start, self.stop, self.duration = self._param_to_modules(
            [start, stop, duration]
        )
        self.cur_x = 0

    def get(self, indexes, input):
        b = self.start.get(indexes, input)
        a = (self.stop.get(indexes, input) - self.start.get(indexes, input)) / (self.duration.get(indexes, input)*parameters.SAMPLING_FREQUENCY)
        xs = np.arange(self.cur_x, self.cur_x + parameters.SAMPLES_PER_FRAME)
        self.cur_x += parameters.SAMPLES_PER_FRAME
        return b + xs * a
