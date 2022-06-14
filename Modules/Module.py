import numpy as np
from Modules.Constant import Constant


class Module:
    def __init__(self):
        self.is_dynamic = False
        self.current_sample = 0

    def _param_to_modules(self, params_array):
        for i, x in enumerate(params_array):
            if not isinstance(x, Module) and not isinstance(x, Constant):
                params_array[i] = Constant(x)
            else:
                self.is_dynamic = True
        return params_array

    def _get_next_times(self, input_size):
        times = np.arange(self.current_sample, self.current_sample+input_size) /SAMPLING_FREQUENCY
        self.current_sample += input_size
        return times

    def _reset(self):
        self.current_sample = 0

    def get(self, input):
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

    def get(self, input):
        if self.op == "+":
            return self.first.get(input) + self.second.get(input)
        elif self.op == "-":
            return self.first.get(input) - self.second.get(input)
        elif self.op == "*":
            return self.first.get(input) * self.second.get(input)
        elif self.op == "/":
            return self.first.get(input) / self.second.get(input)
