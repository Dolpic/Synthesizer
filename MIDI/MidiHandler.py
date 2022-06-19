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
            # format is [[[status, data1, data2, data3], timestamp]]
            status, key, velocity, _ = input.read(1)[0][0]

            if DEBUG:
                print_midi(status, key, velocity)

            velocity = (velocity - MIDI_LOWEST_VELOCITY) / (
                MIDI_HIGHEST_VELOCITY - MIDI_LOWEST_VELOCITY
            )

        else:
            status, key, velocity = (None,None,None)

        keys_amps = current_script.miditofreq.process(status, key, velocity)

        result = [
                self.past_data[1][self.past_data[0].index((key, amp))] if (key, amp) in self.past_data[0] else
                (midi_to_frequency(key, self.memory), amp, key)
                for key, amp in keys_amps
            ]
        

        for freq_and_dev, amp, note in result:
            self.memory.add(freq_and_dev[1], amp, note)

        self.past_data = (keys_amps, result)

        return np.asarray([(freq_and_dev[0], amp) for freq_and_dev, amp, note in result])

    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)
