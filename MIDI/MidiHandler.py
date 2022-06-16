import math
import numpy as np
from parameters import DEBUG, MIDI_NOTHING
from MIDI.midi_utils import midi_to_frequency, print_midi
from MIDI.filters.Arpeggiator import Arpeggiator
#from MIDI.filters.Envelope import Envelope
from MIDI.filters.Default import Default
from MIDI.Memory import *

class MidiHandler:
    arp = Arpeggiator()
    default = Default()
    memory = Memory()

    def process(self, input):
        if input.poll():
            status, note, velocity, _ = input.read(1)[0][0]
            if DEBUG:
                print_midi(status, note, velocity)
        else:
            status, note, velocity = MIDI_NOTHING, MIDI_NOTHING, MIDI_NOTHING

        current_notes = self.apply_filter(status, note, velocity / 127)

        result = np.asarray(
            [
                (midi_to_frequency(note, self.memory), amplitude, note)
                for note, amplitude in current_notes
            ]
        )

        for freq_and_dev, amp, note in result:
            if not self.memory.contains(freq_and_dev[1], amp, note):
                self.memory.add(freq_and_dev[1], amp, note)

        return np.asarray([(freq_and_dev[0], amp, note) for freq_and_dev, amp, note in result])

    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)
