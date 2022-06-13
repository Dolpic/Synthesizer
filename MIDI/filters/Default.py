import numpy as np
from parameters import MIDI_DOWN, MIDI_UP
from MIDI.midi_utils import is_piano_key


class Default:

    def __init__(self):
        self.keys_down = {}
        self.velocities = np.empty(0)
        self.notes = np.empty(0)

    def process(self, status, note, velocity):
        if is_piano_key(note):
            if status == MIDI_DOWN:
                self.keys_down[note] = velocity
            elif status == MIDI_UP:
                try:
                    self.keys_down.pop(note)
                except KeyError:
                    # May happen when changing keys too fast. Just ignore it. The key is gone anyway.
                    pass

        self.velocities = np.asarray(list(self.keys_down.values()), dtype='float32')
        self.notes      = np.asarray(list(self.keys_down.keys()),   dtype='float32')

        return list(zip(self.notes, self.velocities))
