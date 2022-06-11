from parameters import *
import numpy as np
from Modules.Module import *

class Reverb(Module):
    audible_limit = 0.001

    def __init__(self, delay, dampening=0.5):
        params = self._param_to_modules([delay, dampening])
        self.delay      = params[0]
        self.dampening  = params[1]

        self.reverbs = []

    def get(self, input):
        result = input
        to_remove = []

        for entry in self.reverbs:
            entry["delay"] -= len(input)
            if(entry["delay"] <= 0):
                result += entry["data"] * np.maximum(1-self.dampening.get(input), 0)
                to_remove.append(entry)

        if not self._is_data_inaudible(input):
            self.reverbs.append({
                "delay" : self.delay.get(input)[0]*SAMPLING_FREQUENCY,
                "data" : input
            })

        for x in to_remove:
            self.reverbs.remove(x)

        return result

    def _is_data_inaudible(self, data):
        return np.max(data) < self.audible_limit and np.min(data) > -self.audible_limit