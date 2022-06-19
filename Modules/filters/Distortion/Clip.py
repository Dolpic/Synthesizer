import numpy as np

from Modules.Module import Module


"""
Clip distortion
This filter simulates clipping sounds, carateristic of amplification beyond limits.

The formula is adapted from https://ccrma.stanford.edu/~jos/pasp/Soft_Clipping.html


Starting from the expression f(x) = x/i - x^j/k for some constants i,j and k.
We wanted the following parameters :
- A limit l (2/3 in the website above) 
- A "hardness" factor h, the higher this parameter the closer the filter will be to a hard clip filter.

We imposed the constraints :
f(l) = l 
f'(l) = 0

Solving the constraints leads to the following expression:
f(x) = l*h/(h-1) * (x/l - x^h/l^h*h)

This gives us a nice parametrized curve for x between 0 and l. For negative values its sign is reversed.

"""

class Clip(Module):
    def __init__(self, limit, hardness=0):
        self.limit, self.hardness = self._param_to_modules([limit, hardness])

    def get(self, indexes, input):
        l = self.limit.get(indexes, input)
        h = self.hardness.get(indexes, input)

        input = np.where(input > l, l, input)
        input = np.where(input < -l, -l, input)


        if h.all() <= 0 :
            return input
        else :
            sign = np.sign(input)
            input *= sign
            input = (l * h)/(h - 1) * (input/l - (input**h)/((l**h)*h))
            return input * sign
