import numpy as np
import math

from parameters import SAMPLES_PER_FRAME, SAMPLING_FREQUENCY
from Modules.Module import Module

"""
Module implementing an exponential function.

This module applies an exponential function on the given indexes.
The exponential function start at a given value and reaches an end 
value after a given time in seconds.

Parameters :
start : starting value of the function
stop : end value of the function
duration : duration in seconds to go from the start value to the end value

"""

class Exponential(Module):

    exponential_limit = 1/1000

    def __init__(self, start, stop, duration):
        self.start, self.stop, self.duration = self._param_to_modules(
            [start, stop, duration]
        )
        self.cur_x = 0

    def get(self, indexes, input):
        start = self.start.get(indexes, input)
        stop = self.stop.get(indexes, input)
        last_x = self.duration.get(indexes, input)[0]*SAMPLING_FREQUENCY
        force = math.log(self.exponential_limit)/last_x

        xs = np.arange(self.cur_x, self.cur_x + SAMPLES_PER_FRAME)
        self.cur_x += SAMPLES_PER_FRAME
        return stop + (start-stop)*np.exp(force*xs)
