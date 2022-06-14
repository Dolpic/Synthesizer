import numpy as np
import math
import copy

from parameters import *
from Modules.Module import *
from Modules.Constant import *

class ADSR(Module):
    def __init__(self, 
        attack_time,  attack_func, 
        decay_time,   decay_func, 
                      sustain_func, 
        release_time, release_func
    ):
        super().__init__()
        params = self._param_to_modules([
            attack_time,  attack_func, 
            decay_time,   decay_func, 
                          sustain_func, 
            release_time, release_func
        ])
        self.attack_time  = params[0]
        self.attack_func  = params[1]
        self.decay_time   = params[2]
        self.decay_func   = params[3]
        self.sustain_func = params[4]
        self.release_time = params[5]
        self.release_func = params[6]
        self.status = {}
        self.previous_freq = []

    def _set_entry(self, freq, state, func, nb_samples):
        self.status[freq]['state'] = state
        self.status[freq]['func'] = copy.deepcopy(func)
        self.status[freq]['remaining_samples'] = nb_samples*SAMPLING_FREQUENCY


    def get(self, frequencies):
        result = []
        times = self._get_next_times(SAMPLES_PER_FRAME)
        
        for freq, amp in frequencies:
            if freq not in self.previous_freq:
                self.status[freq] = {
                    "state" : "attack",
                    "func" : copy.deepcopy(self.attack_func),
                    "remaining_samples" : self.attack_time.get(times)[0]*SAMPLING_FREQUENCY,
                    "amp" : self._param_to_modules([amp])[0]
                }

        to_delete = []
        for freq, elem in self.status.items():
            elem["remaining_samples"] -= SAMPLES_PER_FRAME
            amp_mult = elem["func"].get(times)
            amp = elem["amp"].get(times)

            if freq not in frequencies and elem["state"] != "release":
                self._set_entry(freq, "release", self.release_func, self.release_time.get(times)[0])

            elif elem["remaining_samples"] <= 0:

                if elem["state"] == "attack":
                    self._set_entry(freq, "decay", self.decay_func, self.decay_time.get(times)[0])
                elif elem["state"] == "decay":
                    self._set_entry(freq, "sustain", self.sustain_func, math.inf)
                elif elem["state"] == "release":
                    to_delete.append(freq)

            result.append((freq, Constant(amp*amp_mult)))

        for cur in to_delete:
            del self.status[cur]

        self.previous_freq = frequencies

        return result
