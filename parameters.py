"""
PARAMETERS
"""

INPUT_MIDI_DEVICE = 1
OUTPUT_DEVICE = "pulse"  # sd.default.device

DEBUG = False
SAMPLING_FREQUENCY = 44100
NYQUIST_FREQUENCY = SAMPLING_FREQUENCY/2
SAMPLES_PER_FRAME = 512

GENERAL_VOLUME = 0.1

# 0 = Equal Temperament
# 1 = Pythagorean Tuning
# 2 = Just Intonation
TEMPERAMENT = 0

REF_NOTE = 69  # midi code of A4
REF_FREQUENCY = 440  # frequency of A4

"""
EQUAL TEMPERAMENT
"""
PARAM_NB_NOTES_IN_SCALE = 12  # how many notes in an octave (for ET only. always 12 for PT and JI)
PARAM_OCTAVE_FREQUENCY_RATIO = 2  # frequency ratio of an octave (for ET - always 2 for PT and JI)

"""
JUST INTONATION
"""
FIX_PITCH = True  # fix pitch drifting for just intonation
PITCH_CORRECTION_FACTOR = 0.35  # ratio of pitch drift canceled at each iteration of fix (0.35 works well)

"""
GUI
"""

WINDOW_REFRESH_RATE = 45
