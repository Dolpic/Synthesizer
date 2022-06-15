import numpy as np
from parameters import SAMPLING_FREQUENCY
from Modules.Filters.Biquad.Biquad import Biquad


class Notch(Biquad):
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
        b0 = 1
        b1 = -2 * cos_w0
        b2 = 1

        self.c = np.array([b0, b1, b2, a1, a2]) / a0
