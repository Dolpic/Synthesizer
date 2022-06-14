import numpy as np
import time

from parameters import *
from Modules.Module import *

class Biquad(Module):
    def __init__(self, c=[0,0,0,0,0]):
        super().__init__()
        l = SAMPLES_PER_FRAME
        self.c = [c[0]*l, c[1]*l, c[2]*l, c[3]*l, c[4]*l]
        self.x_prev = 0
        self.x_prev_prev = 0
        self.y_prev = 0
        self.y_prev_prev = 0

    def _set_f0_Q(self, f0, Q, gain=0):
        params = self._param_to_modules([f0, Q, gain])
        self.f0 = params[0]
        self.Q  = params[1]
        self.gain = params[2]
        self._update_c([0]*SAMPLES_PER_FRAME)

    def _update_c(self, input):
        raise Exception("_update_c must be implemented")

    def get(self, input):
        result = [] # Using a numpy array is MUCH slower

        if self.is_dynamic:
            self._update_c(input)

        c = self.c
        for i, x in enumerate(input):
            val = c[0][i]*x + c[1][i]*self.x_prev + c[2][i]*self.x_prev_prev - c[3][i]*self.y_prev - c[4][i]*self.y_prev_prev
            result.append(val)
            self.x_prev_prev = self.x_prev
            self.x_prev = x
            self.y_prev_prev = self.y_prev
            self.y_prev = val
        return np.array(result)
