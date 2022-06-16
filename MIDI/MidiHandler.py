import numpy as np

from parameters import DEBUG
import current_script

from MIDI.utils import midi_to_frequency_eqtemp, print_midi
from MIDI.constants import MIDI_HIGHEST_VELOCITY, MIDI_LOWEST_VELOCITY


class MidiHandler:
    def process(self, input):
        if input.poll():
            status, key, velocity, _ = input.read(1)[0][0]

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

        return np.asarray(
            [
                (midi_to_frequency_eqtemp(key), amplitude)
                for key, amplitude in key_amplitude_tuples
            ]
        )
