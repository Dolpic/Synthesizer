import numpy as np
from parameters import SAMPLING_FREQUENCY
from Modules.filters.Biquad.Biquad import Biquad

"""
Bandpass filter

This filter is a biquad filter with :
f0 : The middle frequency of the passing band
Q : The force of the filter

The biquand coefficients are taken from:
https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html

"""

class BandPass(Biquad):
    def __init__(self, f0, Q):
        super().__init__()
        super()._set_f0_Q(f0, Q)

    def _update_c(self, indexes, input):
        Q = self.Q.get(indexes, input)
        w0 = 2 * np.pi * (self.f0.get(indexes, input)) / SAMPLING_FREQUENCY
        alpha = np.sin(w0 / (2 * Q))
        cos_w0 = np.cos(w0)
        a0 = 1 + alpha
        a1 = -2 * cos_w0
        a2 = 1 - alpha
        b0 = alpha*Q
        b1 = 0
        b2 = -alpha*Q

        self.c = [b0/a0, b1/a0, b2/a0, a1/a0, a2/a0]
