import numpy as np
from scipy import signal

from Modules.Module import *

class Oscillator(Module):
    current_sample = 0

    def set(self, freq, amp=1, offset=0, duty=0.5):
        params = self._param_to_modules([freq, amp, duty, offset])
        self.freq   = params[0]
        self.amp    = params[1]
        self.duty   = params[2]
        self.offset = params[3]
        return self

    def _get_next_times(self, input_size):
        times = np.arange(self.current_sample, self.current_sample+input_size) / SAMPLING_FREQUENCY
        self.current_sample += input_size
        return times

class Sine(Oscillator):
    def __init__(self, freq=0, amp=1, offset=0):
        self.set(freq, amp=amp, offset=offset)

    def get(self, x):
        x = self._get_next_times(len(x))
        return np.sin(2*np.pi * self.freq.get(x) * x)*self.amp.get(x) + self.offset.get(x)

class Square(Oscillator):
    def __init__(self, freq=0, amp=1, duty=0.5, offset=0):
        self.set(freq, amp=amp, offset=offset, duty=duty)

    def get(self, x):
        x = self._get_next_times(len(x))
        return signal.square(2*np.pi * self.freq.get(x) * x, duty=self.duty.get(x))*self.amp.get(x) + self.offset.get(x)

class Sawtooth(Oscillator):
    def __init__(self, freq=0, amp=1, width=0, offset=0):
        self.set(freq, amp=amp, offset=offset, duty=width)

    def get(self, x):
        x = self._get_next_times(len(x))
        return signal.sawtooth(2*np.pi * self.freq.get(x) * x, self.duty.get(x))*self.amp.get(x) + self.offset.get(x)

class Triangle(Sawtooth):
    def __init__(self, freq=0, amp=1, offset=0):
        super().__init__(freq=freq, amp=amp, width=0.5, offset=offset)