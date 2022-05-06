import numpy as np
from scipy import signal

class Oscillators:

    @staticmethod
    def Sine(x, frequency, amp=1):
        return np.sin(2*np.pi * frequency * x)*amp

    @staticmethod
    def Sawtooth(x, frequency, amp=1):
        return signal.sawtooth(2*np.pi * frequency * x)*amp

    def Square(x, frequency, duty=0.5, amp=1):
        return signal.square(2*np.pi * frequency * x, duty=duty)*amp

    #TODO Implement : Triangle and others