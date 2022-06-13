import numpy as np

from parameters import *
from Modules.Constant import *


class Module:
    is_dynamic = False

    def _param_to_modules(self, params_array):
        for i, x in enumerate(params_array):
            if not isinstance(x, Module):
                params_array[i] = Constant(x)
            else:
                self.is_dynamic = True
        return params_array

    def get(self, input):
        raise NotImplementedError()
