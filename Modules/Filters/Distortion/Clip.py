import numpy as np

from Modules.Module import Module


class Clip(Module):
    def __init__(self, limit, hardness):
        self.limit, self.hardness = self._param_to_modules([limit, hardness])

    def get(self, input):
        limit = self.limit.get(input)
        input = np.where(input > limit, limit, input)
        input = np.where(input < -limit, -limit, input)

        # Adapted from https://ccrma.stanford.edu/~jos/pasp/Soft_Clipping.html
        h = self.hardness.get(input)
        return limit * h / (h - 1) * (input - (input**h) / h)
