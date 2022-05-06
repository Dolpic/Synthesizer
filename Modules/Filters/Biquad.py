import numpy as np

class Biquad:

    a = []
    b = []
    c = []

    x_prev = 0
    x_prev_prev = 0
    y_prev = 0
    y_prev_prev = 0

    def __init__(self, b0, b1, b2, a0, a1, a2):
        self.a = [a0, a1, a2]
        self.b = [b0, b1, b2]
        self.c = [b0/a0, b1/a0, b2/a0, a1/a0, a2/a0]

    def process(self, input):
        result = np.empty(0)
        c = self.c
        for x in input:
            val = c[0]*x + c[1]*self.x_prev + c[2]*self.x_prev_prev - c[3]*self.y_prev - c[4]*self.y_prev_prev
            result = np.append(result, val)
            self.x_prev_prev = self.x_prev
            self.x_prev = x
            self.y_prev_prev = self.y_prev
            self.y_prev = val
        return result
