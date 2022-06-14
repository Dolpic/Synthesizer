import numpy as np
from parameters import SAMPLING_FREQUENCY
from Modules.Filters.Biquad.Biquad import Biquad


class HighPass(Biquad):
    def __init__(self, f0, Q):
        super()._set_f0_Q(f0, Q)

    def _update_c(self, indexes, input):
        w0 = 2 * np.pi * (self.f0.get(indexes, input)) / SAMPLING_FREQUENCY
        alpha = np.sin(w0 / (2 * self.Q.get(indexes, input)))
        cos_w0 = np.cos(w0)
        a0 = 1 + alpha
        a1 = -2 * cos_w0
        a2 = 1 - alpha
        b0_b2 = (1 + cos_w0) / 2
        b1 = -1 - cos_w0

        self.c = np.array([b0_b2, b1, b0_b2, a1, a2]) / a0
