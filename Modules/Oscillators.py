import numpy as np
from scipy import signal

class Oscillators:

    @staticmethod
    def Sine(x, frequency, amp=1):
        return np.sin(frequency * x*2*np.pi)*amp
    @staticmethod

    def Sawtooth(x, frequency, amp=1):
        return signal.sawtooth(frequency * x*2*np.pi)*amp

    #TODO Implement : Square, Triangle and others