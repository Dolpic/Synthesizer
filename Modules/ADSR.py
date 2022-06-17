import math
import copy

from parameters import SAMPLES_PER_FRAME, SAMPLING_FREQUENCY
from Modules.Module import Module
from Modules.Constant import Constant


class ADSR(Module):
    def __init__(
        self,
        attack_time, attack_func,
        decay_time, decay_func,
        sustain_func,
        release_time, release_func,
    ):
        (
        self.a_time, self.a_func,
        self.d_time, self.d_func,
        self.s_func,
        self.r_time, self.r_func,
        ) = self._param_to_modules([
            attack_time, attack_func,
            decay_time, decay_func,
            sustain_func,
            release_time, release_func
        ])

        self.status = {}
        self.previous_freq = []

    def _set_entry(self, freq, state, func, nb_samples):
        self.status[freq]["state"] = state
        self.status[freq]["func"] = copy.deepcopy(func)
        self.status[freq]["remaining_samples"] = nb_samples * SAMPLING_FREQUENCY

    def get(self, indexes, freq_amp):
        frequencies = list(zip(*freq_amp))[0] if len(list(zip(*freq_amp))) != 0 else []
        result = []

        for freq, amp in freq_amp:
            if freq not in self.previous_freq:
                self.status[freq] = {
                    "state": "attack",
                    "func": copy.deepcopy(self.a_func),
                    "remaining_samples": self.a_time.get(indexes, indexes)[0] * SAMPLING_FREQUENCY,
                    "amp": self._param_to_modules([amp])[0],
                }

        to_delete = []
        for freq, elem in self.status.items():
            elem["remaining_samples"] -= SAMPLES_PER_FRAME
            amp = elem["amp"].get(indexes, indexes)
            amp_mult = elem["func"].get(indexes, indexes)

            if freq not in frequencies and elem["state"] != "release":
                self.status[freq]["interpolation"] = amp_mult / copy.deepcopy(self.r_func).get(indexes, indexes)
                self._set_entry(freq, "release", self.r_func, self.r_time.get(indexes, indexes)[0])

            elif elem["remaining_samples"] <= 0:
                if elem["state"] == "attack":
                    self._set_entry(freq, "decay", self.d_func, self.d_time.get(indexes, indexes)[0])
                elif elem["state"] == "decay":
                    self._set_entry(freq, "sustain", self.s_func, math.inf)
                elif elem["state"] == "release":
                    to_delete.append(freq)

            if "interpolation" in elem.keys():
                amp_mult *= elem["interpolation"]

            result.append([freq, amp * amp_mult])

        for cur in to_delete:
            del self.status[cur]

        self.previous_freq = frequencies

        return result
