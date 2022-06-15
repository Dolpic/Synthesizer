import numpy as np
from scipy import signal

from Modules.Module import Module
from parameters import *

class Oscillator(Module):
    def set(self, freq, amp=1, offset=0, duty=0.5):
        self.freq, self.amp, self.duty, self.offset = self._param_to_modules(
            [freq, amp, duty, offset]
        )
        return self


class Sine(Oscillator):
    def __init__(self, freq=0, amp=1, offset=0):
        self.set(freq=freq, amp=amp, offset=offset)

    def get(self, indexes, input):
        return np.sin(2 * np.pi * self.freq.get(indexes, input) * indexes/SAMPLING_FREQUENCY) * self.amp.get(
            indexes, input
        ) + self.offset.get(indexes, input)


class Square(Oscillator):
    def __init__(self, freq=0, amp=1, duty=0.5, offset=0):
        self.set(freq=freq, amp=amp, offset=offset, duty=duty)

    def get(self, indexes, input):
        return signal.square(
            2 * np.pi * self.freq.get(indexes, input) * indexes/SAMPLING_FREQUENCY, duty=self.duty.get(indexes, input)
        ) * self.amp.get(indexes, input) + self.offset.get(indexes, input)


class Sawtooth(Oscillator):
    def __init__(self, freq=0, amp=1, width=0, offset=0):
        self.set(freq=freq, amp=amp, offset=offset, duty=width)

    def get(self, indexes, input):
        return signal.sawtooth(
            2 * np.pi * self.freq.get(indexes, input) * indexes/SAMPLING_FREQUENCY, self.duty.get(indexes, input)
        ) * self.amp.get(indexes, input) + self.offset.get(indexes, input)


class Triangle(Sawtooth):
    def __init__(self, freq=0, amp=1, offset=0):
        super().__init__(freq=freq, amp=amp, width=0.5, offset=offset)
