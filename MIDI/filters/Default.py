import numpy as np
from MIDI.constants import MIDI_UP, MIDI_DOWN
from MIDI.utils import is_piano_key, parse_status


class Default:
    def __init__(self, voices=None):
        self.keys_down = {}
        self.velocities = np.empty(0)
        self.notes = np.empty(0)
        self.voices = voices

    def pop_key(self, key):
        try:
            self.keys_down.pop(key)
        except KeyError:
            pass

    def push_key(self, key, velocity):
        if self.voices and len(self.keys_down) >= self.voices:
            return

        self.keys_down[key] = velocity

    def process(self, status, note, velocity):
        status, channel = parse_status(status)

        if is_piano_key(note):
            if status == MIDI_DOWN:
                if velocity == 0:
                    self.pop_key(note)  # fun: https://stackoverflow.com/a/43322203
                else:
                    self.push_key(note, velocity)

            elif status == MIDI_UP:
                self.pop_key(note)

        self.velocities = np.asarray(list(self.keys_down.values()), dtype="float32")
        self.notes = np.asarray(list(self.keys_down.keys()), dtype="float32")

        return list(zip(self.notes, self.velocities))
