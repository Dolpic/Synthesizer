import math
import copy

from parameters import SAMPLES_PER_FRAME, SAMPLING_FREQUENCY
from Modules.Module import Module
from Modules.Constant import Constant

"""
ADSR Enveloppe

Brings an Attack - Decay - Sustain - Release enveloppe to a set of frequencies

When a key is pressed the attack phase begin for the given duration, then the 
decay phase is played directly after it for the given duration.
After the decay phase the sustain function is played until the key is released.
On key release, the release function is player for the given duration.

Parameters :
attack_time : time in seconds of the attack phase
attack_func : function used during attack time
decay_time  : time in seconds of the decay phase
decay_time  : function used during attack time
sustain_func : function used during sustain time
release_time : time in seconds of the release phase
release_func : function used during release time

Notes :
To avoid disgracious clicking sound when a key is released before it reaches its 
sustain state, we implemented an interpolation feature.
When a key is released, the amplitude of the frequency will follow the release 
function proportionnaly to its amplitude at the moment of the key release. This
avoids a jump in the amplitude to the release function without taking into account
the current frequency amplitude.

"""

class ADSR(Module):
    def __init__(
        self,
        attack_time,
        attack_func,
        decay_time,
        decay_func,
        sustain_func,
        release_time,
        release_func,
    ):
        (
            self.a_time,
            self.a_func,
            self.d_time,
            self.d_func,
            self.s_func,
            self.r_time,
            self.r_func,
        ) = self._param_to_modules(
            [
                attack_time,
                attack_func,
                decay_time,
                decay_func,
                sustain_func,
                release_time,
                release_func,
            ]
        )

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
                    "remaining_samples": self.a_time.get(indexes, indexes)[0]
                    * SAMPLING_FREQUENCY,
                    "amp": self._param_to_modules([amp])[0],
                }

        to_delete = []
        for freq, elem in self.status.items():

            elem["remaining_samples"] -= SAMPLES_PER_FRAME
            amp = elem["amp"].get(indexes, indexes)
            amp_mult = elem["func"].get(indexes, indexes)

            if freq not in frequencies and elem["state"] != "release":
                r_func_value = copy.deepcopy(self.r_func).get(indexes, indexes)
                self.status[freq]["interpolation"] = amp_mult / r_func_value if r_func_value.any() != 0 else 0
                self._set_entry(freq, "release", self.r_func, self.r_time.get(indexes, indexes)[0])

            elif elem["remaining_samples"] <= 0:
                if elem["state"] == "attack":
                    self._set_entry(
                        freq, "decay", self.d_func, self.d_time.get(indexes, indexes)[0]
                    )
                elif elem["state"] == "decay":
                    self._set_entry(freq, "sustain", self.s_func, math.inf)
                elif elem["state"] == "release":
                    to_delete.append(freq)

            if "interpolation" in elem.keys():
                amp_mult = amp_mult * elem["interpolation"]

            result.append([freq, amp * amp_mult])

        for cur in to_delete:
            del self.status[cur]

        self.previous_freq = frequencies

        return result
