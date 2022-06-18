import numpy as np
from MIDI.constants import MIDI_UP, MIDI_DOWN
from MIDI.utils import is_piano_key, parse_status


class Default:
    def __init__(self):
        self.keys_down = {}
        self.velocities = np.empty(0)
        self.notes = np.empty(0)

    def pop_key(self, key):
        try:
            self.keys_down.pop(key)
        except KeyError:
            # May happen when changing keys too fast. Just ignore it. The key is gone anyway.
            pass

    def process(self, status, note, velocity):
        status, channel = parse_status(status)

        if is_piano_key(note):
            if status == MIDI_DOWN:
                if velocity == 0:
                    self.pop_key(note)  # fun: https://stackoverflow.com/a/43322203
                else:
                    self.keys_down[note] = velocity

            elif status == MIDI_UP:
                self.pop_key(note)

        self.velocities = np.asarray(list(self.keys_down.values()), dtype="float32")
        self.notes = np.asarray(list(self.keys_down.keys()), dtype="float32")

        return list(zip(self.notes, self.velocities))
