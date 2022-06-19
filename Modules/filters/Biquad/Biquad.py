import numpy as np
from parameters import SAMPLES_PER_FRAME
from Modules.Module import Module


"""
Biquad filter

This class serves as a basis to implement all the Biquad filters family.
It can be initialized directly with a parameter c, where c = [
    b0/a0, 
    b1/a0, 
    b2/a0, 
    a1/a0, 
    a2/a0
]

The filter is based on the Biquad formula  
y[n] = c0*x[n] + c1*x[n-1] + c2*x[n-2] - c3*y[n-1] - c4*y[n-2]

Reference :
https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html
"""

class Biquad(Module):
    def __init__(self, c=[0, 0, 0, 0, 0]):
        self.c = list(map(lambda c_i: c_i*SAMPLES_PER_FRAME, c))
        self.x_prev = 0
        self.x_prev_prev = 0
        self.y_prev = 0
        self.y_prev_prev = 0

    def _set_f0_Q(self, f0, Q, gain=0):
        self.f0, self.Q, self.gain = self._param_to_modules([f0, Q, gain])
        self._update_c([0] * SAMPLES_PER_FRAME, [0] * SAMPLES_PER_FRAME)

    def _update_c(self, indexes, input):
        raise NotImplementedError()

    def get(self, indexes, input):
        result = []  # Using a numpy array is MUCH slower

        if self.is_dynamic:
            self._update_c(indexes, input)

        c = self.c
        for i, x in enumerate(input):
            val = (
                c[0][i] * x
                + c[1][i] * self.x_prev
                + c[2][i] * self.x_prev_prev
                - c[3][i] * self.y_prev
                - c[4][i] * self.y_prev_prev
            )
            result.append(val)
            self.x_prev_prev = self.x_prev
            self.x_prev = x
            self.y_prev_prev = self.y_prev
            self.y_prev = val
        return np.array(result)
