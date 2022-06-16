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
    past_data = []

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
                self.past_data[1][self.past_data[0].index(note_amplitude)] if note_amplitude in self.past_data[0] else
                (midi_to_frequency(note_amplitude[0], self.memory), note_amplitude[1], note_amplitude[0])
                for note_amplitude in current_notes
            ]
        )

        for freq_and_dev, amp, note in result:
            self.memory.add(freq_and_dev[1], amp, note)

        self.past_data = (current_notes, result)

        return np.asarray([(freq_and_dev[0], amp, note) for freq_and_dev, amp, note in result])

    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)
