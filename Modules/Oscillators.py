import numpy as np
from scipy import signal

class Sine:
    def __init__(self, freq, amp=1):
        self.freq = freq
        self.amp  = amp

    def get(self, x):
        return np.sin(2*np.pi * self.freq * x)*self.amp


class Square:
    def __init__(self, freq, duty=0.5, amp=1):
        self.freq = freq
        self.amp  = amp
        self.duty = duty

    def get(self, x):
        return signal.square(2*np.pi * self.freq * x, duty=self.duty)*self.amp


class Sawtooth:
    def __init__(self, freq, amp=1):
        self.freq = freq
        self.amp  = amp

    def get(self, x):
        return signal.sawtooth(2*np.pi * self.freq * x)*self.amp