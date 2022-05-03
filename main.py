import pygame.midi
import numpy as np
import sounddevice as sd

from MIDI.MidiHandler import MidiHandler
from Modules.Oscillators import Oscillators

"""
PARAMETERS
"""
INPUT_MIDI_DEVICE    = 1
OUTPUT_DEVICE        = 'pulse'#sd.default.device

DEBUG                = True
SAMPLING_FREQUENCY   = 44100 
NB_SAMPLES_PER_FRAME = 1024

"""
INIT
"""
pygame.midi.init()
sd.default.device = OUTPUT_DEVICE
input_device = pygame.midi.Input(INPUT_MIDI_DEVICE)
audio_stream = sd.OutputStream(channels=2)

"""
FUNCTIONS
"""
def process_output(times):
    return Oscillators.Sine(times, 340)

def run():
    is_running = True
    current_sample = 0
    audio_stream.start()

    while is_running:

        MidiHandler.handle(input_device)

        frame_times = np.arange(current_sample, current_sample+NB_SAMPLES_PER_FRAME)
        times = frame_times / SAMPLING_FREQUENCY
        right, left = process_output(times)     
        audio_stream.write(np.column_stack( (right, left) ).astype('float32'))
        current_sample += NB_SAMPLES_PER_FRAME

run()

