import numpy as np
from parameters import *
from Modules.Filters.Biquad.Biquad import *

class HighShelf(Biquad):
    def __init__(self, f0, Q, gain):
        super()._set_f0_Q(f0, Q, gain)
    
    def _update_c(self, input):
        w0 = 2*np.pi*(self.f0.get(input))/SAMPLING_FREQUENCY
        alpha = np.sin(w0/(2*self.Q.get(input)))
        A = 10 ** (self.gain.get(input) / 40)   

        cos_w0 = np.cos(w0)
        A_sqrt = np.sqrt(A)
        a0 = (A+1)-(A-1)*cos_w0+2*A_sqrt*alpha
        a1 = 2*((A-1)-(A+1)*cos_w0)
        a2 = (A+1)-(A-1)*cos_w0-2*A_sqrt*alpha
        b0 = A*((A+1)+(A-1)*cos_w0+2*A_sqrt*alpha)
        b1 = -2*A*( (A-1)+(A+1)*cos_w0 )
        b2 = A*( (A+1)+(A-1)*cos_w0-2*A_sqrt*alpha )

        self.c = np.array([b0, b1, b2, a1, a2])/a0