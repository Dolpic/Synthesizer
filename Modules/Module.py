import numpy as np
from Modules.Constant import Constant
from parameters import SAMPLING_FREQUENCY


class Module:
    def _param_to_modules(self, params_array):
        self.is_dynamic = False
        for i, x in enumerate(params_array):
            if not isinstance(x, Module) and not isinstance(x, Constant):
                params_array[i] = Constant(x)
            else:
                self.is_dynamic = True
        return params_array

    def _reset(self):
        self.current_sample = 0

    def get(self, indexes, input):
        raise NotImplementedError()

    def __add__(self, other):
        return Module_Operation(self, other, "+")

    def __sub__(self, other):
        return Module_Operation(self, other, "-")

    def __mul__(self, other):
        return Module_Operation(self, other, "*")

    def __truediv__(self, other):
        return Module_Operation(self, other, "/")


class Module_Operation(Module):
    def __init__(self, first, second, op):
        params = [first, second]
        self._param_to_modules(params)
        self.first = params[0]
        self.second = params[1]
        self.op = op

    def get(self, indexes, input):
        if self.op == "+":
            return self.first.get(indexes, input) + self.second.get(indexes, input)
        elif self.op == "-":
            return self.first.get(indexes, input) - self.second.get(indexes, input)
        elif self.op == "*":
            return self.first.get(indexes, input) * self.second.get(indexes, input)
        elif self.op == "/":
            return self.first.get(indexes, input) / self.second.get(indexes, input)
