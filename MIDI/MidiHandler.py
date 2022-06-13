import numpy as np
from parameters import DEBUG, MIDI_NOTHING
from MIDI.midi_utils import midi_to_frequency_eqtemp, print_midi
from MIDI.filters.Arpeggiator import Arpeggiator
from MIDI.filters.Envelope import Envelope
from MIDI.filters.Default import Default


class MidiHandler:
    arp = Arpeggiator()
    default = Default()
    envelope = Envelope(lambda t: 2*t if t < 0.5 else 2*(1-t), 1.0)  # triagnle envelope

    def process(self, input):
        if input.poll():
            status, note, velocity, _ = input.read(1)[0][0]
            if DEBUG:
                print_midi(status, note, velocity)
        else:
            status, note, velocity = MIDI_NOTHING, MIDI_NOTHING, MIDI_NOTHING

        current_notes = self.apply_filter(status, note, velocity/127)
        return np.asarray(
            [
                (midi_to_frequency_eqtemp(note), amplitude)
                for note, amplitude
                in current_notes
            ]
        )

    def apply_filter(self, status, note, velocity):
        return self.envelope.process(status, note, velocity)
