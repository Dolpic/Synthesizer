import sounddevice as sd
"""
PARAMETERS
"""

INPUT_MIDI_DEVICE = 1
OUTPUT_DEVICE = "pulse" # sd.default.device

DEBUG = False
SAMPLING_FREQUENCY = 44100
NYQUIST_FREQUENCY = SAMPLING_FREQUENCY/2
SAMPLES_PER_FRAME = 512

GENERAL_VOLUME = 0.1

# 0 = Equal Temperament
# 1 = Pythagorean Tuning
# 2 = Just Intonation
TEMPERAMENT = 0

"""
GUI
"""

WINDOW_REFRESH_RATE = 45
