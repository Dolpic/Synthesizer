import numpy as np

"""
Module implementing a constant value.

Usefull for modules arithmetic.
"""

class Constant:
    def __init__(self, value):
        self.value = value

    def get(self, indexes, input):
        if isinstance(self.value, np.ndarray):
            return self.value
        else:
            return np.array([self.value] * len(input))

    def __add__(self, other):
        return Constant_Operation(self, other, "+")

    def __sub__(self, other):
        return Constant_Operation(self, other, "-")

    def __mul__(self, other):
        return Constant_Operation(self, other, "*")

    def __truediv__(self, other):
        return Constant_Operation(self, other, "/")


class Constant_Operation(Constant):
    def __init__(self, first, second, op):
        self.op = op
        self.first = first
        if isinstance(second, Constant):
            self.second = second
        else:
            self.second = Constant(second)

    def get(self, indexes, input):
        if self.op == "+":
            return self.first.get(indexes, input) + self.second.get(indexes, input)
        elif self.op == "-":
            return self.first.get(indexes, input) - self.second.get(indexes, input)
        elif self.op == "*":
            return self.first.get(indexes, input) * self.second.get(indexes, input)
        elif self.op == "/":
            return self.first.get(indexes, input) / self.second.get(indexes, input)
