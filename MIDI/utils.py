import numpy as np
from MIDI.constants import MIDI_LOWEST_KEY, MIDI_HIGHEST_KEY
from parameters import DEBUG, TEMPERAMENT, PARAM_NB_NOTES_IN_SCALE, PARAM_OCTAVE_FREQUENCY_RATIO, REF_NOTE, REF_FREQUENCY

# SETTINGS - DO NOT CHANGE THIS LINE, CHANGE THE CORRESPONDING FIELDS IN PARAMETERS.PY
NB_NOTES_IN_SCALE = PARAM_NB_NOTES_IN_SCALE if TEMPERAMENT == 0 else 12
OCTAVE_FREQUENCY_RATIO = PARAM_OCTAVE_FREQUENCY_RATIO if TEMPERAMENT == 0 else 2


# PYTHAGOREAN TUNING (PT)
PY_RATIOS = [
    1,
    2187 / 2048,
    9 / 8,
    19683 / 16384,
    81 / 64,
    177147 / 131072,
    729 / 512,
    3 / 2,
    6561 / 4096,
    27 / 16,
    59049 / 32768,
    243 / 128,
]

# JUST INTONATION (JI)
JI_CHARACTERISTIC_TIME_SCALE = 3
JI_RATIOS = [
    [1, 1],
    [16, 15],
    [9, 8],
    [6, 5],
    [5, 4],
    [4, 3],
    [45, 32],
    [3, 2],
    [8, 5],
    [5, 3],
    [9, 5],
    [15, 8],
    [2, 1],
]
JI_WEIGHTS = [2 / (np.log2(max(r[0], r[1])) + 2) for r in JI_RATIOS]
JI_PITCH_DEVIATIONS = [
    (1200 * np.log2(JI_RATIOS[i][0] / JI_RATIOS[i][1]) - 100 * i)
    for i in range(len(JI_RATIOS))
]
EPSILON = 0.001


def is_piano_key(key):
    return key is not None and key >= MIDI_LOWEST_KEY and key <= MIDI_HIGHEST_KEY


def print_midi(status, note, velocity):
    print(f"status:{status}, note:{note}, velocity:{velocity}")


def midi_to_frequency(midi_number, memory):
    result = 0
    if TEMPERAMENT == 0:
        result = equal_temperament(midi_number)
    elif TEMPERAMENT == 1:
        result = pythagorean_tuning(midi_number)
    elif TEMPERAMENT == 2:
        result = just_intonation(midi_number, memory)

    if DEBUG:
        print("key in :", midi_number, " => freq :", result[0])
    return result


def equal_temperament(midi_number):
    return (
        np.power(OCTAVE_FREQUENCY_RATIO, (midi_number - REF_NOTE) / NB_NOTES_IN_SCALE)
        * REF_FREQUENCY,
        0,
    )


def pythagorean_tuning(midi_number):
    note = int((midi_number - REF_NOTE) % NB_NOTES_IN_SCALE)
    octave = (midi_number - REF_NOTE - note) / NB_NOTES_IN_SCALE - 1
    return (
        np.power(OCTAVE_FREQUENCY_RATIO, octave)
        * (OCTAVE_FREQUENCY_RATIO * PY_RATIOS[note])
        * REF_FREQUENCY,
        0,
    )


def just_intonation(midi_number, memory):

    # get deviation from ET in cents
    r = range(len(memory.cells))
    a = np.sum([get_time_weight(midi_number, memory, i) for i in r]) + EPSILON
    b = (
        np.sum(
            [
                get_time_weight(midi_number, memory, i)
                * get_time_deviation(midi_number, memory, i)
                for i in r
            ]
        )
    )
    dev = -b / a
    # obtain corresponding frequency
    sol = equal_temperament(midi_number)[0] * np.power(2, dev / 1200)

    # c = np.sum([get_time_weight(midi_number, memory, i) * get_time_deviation(midi_number, memory, i) * get_time_deviation(midi_number, memory, i) for i in range(memory)]) + EPSILON * REF_FREQUENCY * REF_FREQUENCY
    # loss = 0.5 * (c - b * dev)

    return sol, dev


# a key is a tuple note + volume
def get_deviation(key1, key2):
    k = key2 - key1
    i = int(np.abs(k) % (len(JI_WEIGHTS) - 1))
    return np.sign(k) * JI_PITCH_DEVIATIONS[i]


def get_time_deviation(key1, memory, index):
    return get_deviation(key1, memory.cells[index][2]) - memory.cells[index][0]


def get_time_weight(key1, memory, index):
    _, vol, key2 = memory.cells[index]
    k = key2 - key1
    o = 1 + int(np.abs(k) / 12)
    i = int(np.abs(k) % len(JI_WEIGHTS))
    w = JI_WEIGHTS[i] / o * np.power(1.2, vol)
    return np.exp(-index / JI_CHARACTERISTIC_TIME_SCALE) * w


def parse_status(status_16_bits):
    if status_16_bits is None:
        return None, None

    ms_byte = status_16_bits & 0xF0  # wew
    ls_byte = status_16_bits & 0x0F
    return ms_byte, ls_byte
