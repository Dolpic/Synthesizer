import numpy as np
from Modules.Filters.filter_utils import *
from Modules.Module import *
from scipy.signal import iirfilter, sosfilt, sosfilt_zi, lfilter

from parameters import *

class Biquad(Module):

    dynamic = False

    def __init__(self, order, W0, filter_type, W1 = None):
        params = [order, W0, W1, filter_type]
        self.dynamic = initialize_params(params)
        self.order = params[0]
        self.W0 = params[1]
        self.W1 = params[2]
        self.filter_type = params[3]

        self.update_params(0)
        self.zi = sosfilt_zi(self.sos)

    def get(self, input):
        if self.dynamic: 
            result = np.empty(1)
            for x in np.array_split(input, 100):
                self.update_params(x[0])
                tmp, self.zi = sosfilt(self.sos, input, zi=self.zi)
                result = np.append(result, tmp)
            return result
        else :
            result, self.zi = sosfilt(self.sos, input, zi=self.zi)
            return result

    def update_params(self, input=None):
        if self.dynamic:
            #print("VALUE : ", self.W0.get(input)),
            self.sos = iirfilter(
                self.order.get(input), 
                [self.W0.get(input), self.W1.get(input)] if self.W1.get(input) != None else self.W0.get(input)+2000, 
                btype=self.filter_type.get(input),
                fs = SAMPLING_FREQUENCY,
                output='sos'
            )
        else :
            self.sos = iirfilter(
                self.order, 
                [self.W0, self.W1] if self.W1 != None else self.W0,
                btype=self.filter_type, 
                fs = SAMPLING_FREQUENCY,
                output='sos'
            )
            self.zi = sosfilt_zi(self.sos)

class HighPass(Biquad):
    def __init__(self, order, W0):
        super().__init__(order, W0, 'highpass')

class LowPass(Biquad):
    def __init__(self, order, W0):
        super().__init__(order, W0, 'lowpass')

class BandPass(Biquad):
    def __init__(self, order, W0, W1):
        super().__init__(order, W0, 'lowpass', W1)


