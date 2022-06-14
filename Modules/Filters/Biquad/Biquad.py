import numpy as np
from parameters import SAMPLES_PER_FRAME
from Modules.Module import Module


class Biquad(Module):
    def __init__(self, c=[0, 0, 0, 0, 0]):
        super().__init__()
        self.c = list(map(lambda c_i: c_i*SAMPLES_PER_FRAME, c))
        self.x_prev = 0
        self.x_prev_prev = 0
        self.y_prev = 0
        self.y_prev_prev = 0

    def _set_f0_Q(self, f0, Q, gain=0):
        self.f0, self.Q, self.gain = self._param_to_modules([f0, Q, gain])
        self._update_c([0] * SAMPLES_PER_FRAME)

    def _update_c(self, input):
        raise Exception("_update_c must be implemented")

    def get(self, input):
        result = []  # Using a numpy array is MUCH slower

        if self.is_dynamic:
            self._update_c(input)

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
