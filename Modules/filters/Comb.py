from Modules.Module import Module
from parameters import SAMPLES_PER_FRAME
import numpy as np

"""
Feedforward Comb filter

The filter acts like a periodic notch on the frequencies spectrum.

This filter is based on the expression y(n) = x(n) + b*x(n-M)
The parameters are :
g : The force of the filter, generally between 0.5 and 1
M : Filter magnitude, corresponds to the period of the notch effects

Adapted from https://ccrma.stanford.edu/~jos/waveguide/Feedforward_Comb_Filters.html

"""

class Comb(Module):
    def __init__(self, b, M):
        super().__init__()
        (self.b, self.M) = self._param_to_modules([b, M])
        self.previous = np.empty(1)

    def get(self, indexes, input):
        self.previous = np.append(self.previous, input)
        M = -np.clip(self.M.get(indexes, input).astype(int)+SAMPLES_PER_FRAME,0,len(self.previous))+1
        b = self.b.get(indexes, input)

        for i in range(SAMPLES_PER_FRAME):
            input[i] += b[i]*self.previous[M[i]+i+1]

        return input
