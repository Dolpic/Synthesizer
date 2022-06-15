import math
import numpy as np
from parameters import DEBUG, MIDI_NOTHING
from MIDI.midi_utils import midi_to_frequency, print_midi
from MIDI.filters.Arpeggiator import Arpeggiator
#from MIDI.filters.Envelope import Envelope
from MIDI.filters.Default import Default


class MidiHandler:
    arp = Arpeggiator()
    default = Default()
    MEMORY_SIZE = 32
    memory = [[] for i in range(MEMORY_SIZE)]    #TODO check if gud

    def process(self, input):
        if input.poll():
            status, note, velocity, _ = input.read(1)[0][0]
            if DEBUG:
                print_midi(status, note, velocity)
        else:
            status, note, velocity = MIDI_NOTHING, MIDI_NOTHING, MIDI_NOTHING

        current_notes = self.apply_filter(status, note, velocity / 127)
        return np.asarray(
            [
                (midi_to_frequency(note, amplitude, self.memory), amplitude)
                for note, amplitude in current_notes
            ]
        )

    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)
