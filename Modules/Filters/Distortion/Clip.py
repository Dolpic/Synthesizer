import numpy as np

from Modules.Module import Module


class Clip(Module):
    def __init__(self, limit, hardness=0):
        super().__init__()
        self.limit, self.hardness = self._param_to_modules([limit, hardness])

    def get(self, indexes, input):
        l = self.limit.get(indexes, input)
        h = self.hardness.get(indexes, input)

        input = np.where(input > l, l, input)
        input = np.where(input < -l, -l, input)

        # Adapted from https://ccrma.stanford.edu/~jos/pasp/Soft_Clipping.html
        if h.all() <= 0 :
            return input
        else :
            return (l - h)/(h - 1) * (input/l - (input**h)/((l**h)*h))
