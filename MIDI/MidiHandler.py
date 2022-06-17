import numpy as np

from parameters import DEBUG
import current_script

from MIDI.utils import midi_to_frequency, print_midi
from MIDI.constants import MIDI_HIGHEST_VELOCITY, MIDI_LOWEST_VELOCITY
from MIDI.filters.Arpeggiator import Arpeggiator
from MIDI.filters.Default import Default
from MIDI.Memory import Memory

class MidiHandler:
    arp = Arpeggiator()
    default = Default()
    memory = Memory()
    past_data = []

    def process(self, input):
        if input.poll():
            list_of_one_midi_msg = input.read(1)  # format is [[[status, data1, data2, data3], timestamp]]
            status, key, velocity, _ = list_of_one_midi_msg[0][0]

            if DEBUG:
                print_midi(status, key, velocity)

            velocity = (velocity - MIDI_LOWEST_VELOCITY) / (
                MIDI_HIGHEST_VELOCITY - MIDI_LOWEST_VELOCITY
            )

        else:
            status, key, velocity = (
                None,
                None,
                None,
            )

        key_amplitude_tuples = current_script.miditofreq.process(status, key, velocity)

        result = np.asarray(
            [
                self.past_data[1][self.past_data[0].index(note_amplitude)] if note_amplitude in self.past_data[0] else
                (midi_to_frequency(note_amplitude[0], self.memory), note_amplitude[1], note_amplitude[0])
                for note_amplitude in key_amplitude_tuples
            ]
        )

        for freq_and_dev, amp, note in result:
            self.memory.add(freq_and_dev[1], amp, note)

        self.past_data = (key_amplitude_tuples, result)

        return np.asarray([(freq_and_dev[0], amp) for freq_and_dev, amp, note in result])


    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)

