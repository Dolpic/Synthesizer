from parameters import *
import numpy as np

class Reverb:

    def __init__(self, delay, amplitude=0.5, max_repeat=0):
        self.delay = delay*SAMPLING_FREQUENCY
        self.amplitude = amplitude
        self.max_repeat = max_repeat
        self.reverbs = []

    def process(self, input):
        result = input
        to_remove = None

        for entry in self.reverbs:
            entry["delay"] -= len(input)
            if(entry["delay"] <= 0):
                entry["counter"] += 1
                entry["delay"] = self.delay*SAMPLING_FREQUENCY
                if entry["counter"] >= self.max_repeat and self.max_repeat > 0:
                    to_remove = entry
                result += entry["data"]*self.amplitude

        self.reverbs.append({
            "delay" : self.delay,
            "counter" : 0,
            "data" : input
        })

        if to_remove != None:
            self.reverbs.remove(entry)

        return result