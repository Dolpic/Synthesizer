import numpy as np
from parameters import MIDI_LOWER_KEY, MIDI_HIGHER_KEY


def is_piano_key(note):
    return note >= MIDI_LOWER_KEY and note <= MIDI_HIGHER_KEY


def print_midi(status, note, velocity):
    print(f"status:{status}, note:{note}, velocity:{velocity}")


def midi_to_frequency_eqtemp(midi_number):
    REF_NOTE = 69
    REF_FREQUENCY = 440
    NB_NOTES_IN_SCALE = 12
    OCTAVE_FREQUENCY_RATIO = 2
    return np.power(OCTAVE_FREQUENCY_RATIO, (midi_number-REF_NOTE)/NB_NOTES_IN_SCALE) * REF_FREQUENCY
