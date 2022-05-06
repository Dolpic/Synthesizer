import numpy as np
from parameters import *
from Modules.Filters.Biquad import *

class BandPass(Biquad):

    def __init__(self, f0, Q):
        w0 = 2*np.pi*f0/SAMPLING_FREQUENCY
        alpha = np.sin(w0/(2*Q))
        a0 = 1 + alpha
        a1 = -2*np.cos(w0)
        a2 = 1 - alpha
        b0 = np.sin(w0)/2
        b1 = 0
        b2 = -np.sin(w0)/2
        super().__init__(b0,b1,b2,a0,a1,a2)

    