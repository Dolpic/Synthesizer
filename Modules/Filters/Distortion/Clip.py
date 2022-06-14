import numpy as np

from Modules.Module import Module


class Clip(Module):
    def __init__(self, limit, hardness=0):
        self.limit, self.hardness = self._param_to_modules([limit, hardness])

    def get(self, input):
        l = self.limit.get(input)
        print(l)
        input = np.where(input > l, l, input)
        input = np.where(input < -l, -l, input)

        # Adapted from https://ccrma.stanford.edu/~jos/pasp/Soft_Clipping.html
        h = self.hardness.get(input)
        if h.all() <= 0 :
            return input
        else :

            return (l - h)/(h - 1) * (input/l - (input**h)/((l**h)*h))
