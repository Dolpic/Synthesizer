import numpy as np
from parameters import SAMPLING_FREQUENCY
from Modules.filters.Biquad.Biquad import Biquad

"""
Highpass filter

This filter is a biquad filter with :
f0 : The frequency from which higher frequencies will not be diminished
Q : The force of the filter

The biquand coefficients are taken from:
https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html

"""

class HighPass(Biquad):
    def __init__(self, f0, Q):
        super().__init__()
        super()._set_f0_Q(f0, Q)

    def _update_c(self, indexes, input):
        w0 = 2 * np.pi * (self.f0.get(indexes, input)) / SAMPLING_FREQUENCY
        alpha = np.sin(w0 / (2 * self.Q.get(indexes, input)))
        cos_w0 = np.cos(w0)
        a0 = 1 + alpha
        a1 = -2 * cos_w0
        a2 = 1 - alpha
        b0 = (1 + cos_w0) / 2
        b1 = -1 - cos_w0
        b2 = b0

        self.c = [b0/a0, b1/a0, b2/a0, a1/a0, a2/a0]
