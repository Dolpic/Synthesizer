import time
import numpy as np
from parameters import DEBUG, PITCH_CORRECTION_FACTOR


class Memory:
    def __init__(self, size=4, pitch_correction_factor=PITCH_CORRECTION_FACTOR):
        self.cells = []
        self.size = size
        self.pitch_correction_factor = pitch_correction_factor
        self.prev_time = time.time()

    def add(self, dev, amplitude, note):
        index = self.index(amplitude, note)

        if index < 0 : #if memory does not contains this note, add it.
            if len(self.cells) >= self.size:
                self.cells = [[dev, amplitude, note]] + self.cells[:-1]
            else:
                self.cells = [[dev, amplitude, note]] + self.cells
            if DEBUG:
                print("Added new value to memory. It now contains ", self.cells)

        else : #else, put it at index 0 to signify its importance
            self.cells = [[dev, amplitude, note]] + self.cells[:index] + self.cells[index+1:]

    def index(self, amplitude, note):
        result = 0
        for f, a, n in self.cells:
            if amplitude == a and note == n:
                return result
            result += 1
        return -1

    #returns average pitch drift of notes in memeory
    def pitch_drift(self):
        drift = np.average([c for c, _, _ in self.cells]) if len(self.cells) > 0 else 0
        return drift

    def fix_pitch(self):
        new_time = time.time()
        delta = self.pitch_drift() * self.pitch_correction_factor * (self.prev_time - new_time)
        self.cells = [[dev+delta, amp, note] for dev, amp, note in self.cells]
        self.prev_time = new_time
