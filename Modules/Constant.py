import numpy as np

class Constant:
    def __init__(self, value):
        self.value = value

    def get(self, input):
        return np.array([self.value]*len(input))