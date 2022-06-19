from Modules.Module import Module
from parameters import SAMPLES_PER_FRAME
import numpy as np

class Comb(Module):
    def __init__(self, alpha, K):
        super().__init__()
        (self.alpha, self.K) = self._param_to_modules([alpha, K])
        self.previous = np.empty(1)

    def get(self, indexes, input):
        self.previous = np.append(self.previous, input)
        K = -np.clip(self.K.get(indexes, input).astype(int)+SAMPLES_PER_FRAME,0,len(self.previous))+1
        alpha = self.alpha.get(indexes, input)

        for i in range(SAMPLES_PER_FRAME):
            input[i] += alpha[i]*self.previous[K[i]+i+1]

        return input
