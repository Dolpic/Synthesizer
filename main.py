import pygame.midi
import numpy as np
import sounddevice as sd

from parameters import *
from MIDI.MidiHandler import MidiHandler
from Modules.Oscillators import Oscillators
from Modules.Filters.LowPass import *

"""
INIT
"""
pygame.midi.init()
sd.default.device = OUTPUT_DEVICE
input_device = pygame.midi.Input(INPUT_MIDI_DEVICE)
audio_stream = sd.OutputStream(channels=2)
midi_handler = MidiHandler()

"""
FUNCTIONS
"""

lowPass = LowPass(1000, 0.5)

def show_peripherals():
    print("MIDI Inputs : ")
    for i in range(pygame.midi.get_count()):
        (interf, name, input, output, opened) = pygame.midi.get_device_info(i)
        if input : print('   {} : {} - {:<30}  Opened: {}'.format(i, interf.decode(), name.decode(), "yes" if opened else "no"))
    print('\n')
    print("Audio Outputs : ")
    print(sd.query_devices())


def process_output(times, notes):
    GENERAL_VOLUME = 0.2
    outputs = np.zeros(len(times))
    for note, amplitude in notes:
        outputs += Oscillators.Square(times, note, amplitude)
    outputs *= GENERAL_VOLUME

    #Filters
    outputs = lowPass.process(outputs)
    print(outputs)

    return outputs, outputs


def run():
    is_running = True
    current_sample = 0
    audio_stream.start()

    while is_running:
        times = np.arange(current_sample, current_sample+SAMPLES_PER_FRAME) / SAMPLING_FREQUENCY

        notes = midi_handler.handle(input_device)
        right, left = process_output(times, notes)     
        
        audio_stream.write(np.column_stack( (right, left) ).astype('float32'))
        current_sample += SAMPLES_PER_FRAME

#show_peripherals()
run()

