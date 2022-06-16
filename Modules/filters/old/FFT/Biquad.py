from scipy.fft import rfft, irfft

from parameters import *


class LowPass:
    def __init__(self, cut_frequency):
        self.cut_frequency = cut_frequency

    def get(self, input):
        frequencies = rfft(input, n=int(SAMPLING_FREQUENCY / 100))
        output = irfft(frequencies)
        return output
