import numpy as np
from parameters import SAMPLING_FREQUENCY
from Modules.filters.Biquad.Biquad import Biquad

"""
PeakingEQ filter

This filter is a biquad filter with :
f0 : The frequency to peak
Q : The width of the peak, smaller Q means a wider peak in the frequencies

The biquand coefficients are taken from:
https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html

"""

class PeakingEQ(Biquad):
    def __init__(self, f0, Q, gain):
        super().__init__()
        super()._set_f0_Q(f0, Q, gain)

    def _update_c(self, indexes, input):
        w0 = 2 * np.pi * (self.f0.get(indexes, input)) / SAMPLING_FREQUENCY
        alpha = np.sin(w0 / (2 * self.Q.get(indexes, input)))
        A = 10 ** (self.gain.get(indexes, input) / 40)

        cos_w0 = np.cos(w0)
        a0 = 1 + alpha / A
        a1 = -2 * cos_w0
        a2 = 1 - alpha / A
        b0 = 1 + alpha * A
        b1 = -2 * cos_w0
        b2 = 1 - alpha * A

        self.c = [b0/a0, b1/a0, b2/a0, a1/a0, a2/a0]
