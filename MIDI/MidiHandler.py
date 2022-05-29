import numpy as np
from parameters import *
from MIDI.midi_utils import *
from MIDI.filters.Arpeggiator import *
from MIDI.filters.Default import *

class MidiHandler:
    arp = Arpeggiator()
    default = Default()

    def process(self, input):
        if input.poll():
            status, note, velocity, _ = input.read(1)[0][0]
            if DEBUG : print_midi(status, note, velocity)
        else:
            status, note, velocity = MIDI_NOTHING, MIDI_NOTHING, MIDI_NOTHING

        current_notes = self.apply_filter(status, note, velocity/127)
        return np.asarray([(midi_to_frequency(note), amplitude) for note, amplitude in current_notes])

    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)
        