import math
import numpy as np
from parameters import DEBUG, MIDI_NOTHING
from MIDI.midi_utils import midi_to_frequency_eqtemp, print_midi
from MIDI.filters.Arpeggiator import Arpeggiator
from MIDI.filters.Envelope import Envelope
from MIDI.filters.Default import Default


def fun(x):
    return 1 if x < 0.5 else -1


def envelope(type):
    funcs = {
        "lin": lambda t: (2 * fun(t) * (t - 0.5) + 1) * 0.7,
        "sq": lambda t: ((2 * (t - 0.5 + fun(t) * 0.5)) ** 2) * 0.7,
        "exp": lambda t: math.exp(fun(t) * 12 * (t - 0.5)) * 0.7,
    }
    return funcs[type]


class MidiHandler:
    arp = Arpeggiator()
    default = Default()
    envelope = Envelope(envelope("exp"), 1.0)  # triangle envelope

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
                (midi_to_frequency_eqtemp(note), amplitude)
                for note, amplitude in current_notes
            ]
        )

    def apply_filter(self, status, note, velocity):
        return self.default.process(status, note, velocity)
