import sounddevice as sd

"""
PARAMETERS
"""

INPUT_MIDI_DEVICE  = 1
OUTPUT_DEVICE      = 'pulse'#sd.default.device

DEBUG              = False
SAMPLING_FREQUENCY = 44100 
SAMPLES_PER_FRAME  = 128

GENERAL_VOLUME = 0.2

"""
MIDI CONSTANTS
"""

# Status
MIDI_DOWN    = 144
MIDI_UP      = 128
MIDI_NOTHING = -1

# Keys
MIDI_LOWER_KEY  = 0
MIDI_HIGHER_KEY = 127 

"""
GUI
"""

WINDOW_REFRESH_RATE = 30