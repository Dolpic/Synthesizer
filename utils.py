import mido
import pygame.midi
import sounddevice as sd
import parameters
import os


def show_peripherals():
    pygame.midi.init()
    print("PyGame MIDI Inputs : ")
    for i in range(pygame.midi.get_count()):
        (interf, name, input, output, opened) = pygame.midi.get_device_info(i)
        if input:
            print("   {} : {} - {:<30}  Opened: {}".format(
                    i, interf.decode(), name.decode(), "yes" if opened else "no"
            ))
    print("Mido MIDI Outputs : ")
    print(mido.get_output_names())
    print("Audio Outputs : ")
    print(sd.query_devices())

def init():
    sd.default.device = parameters.OUTPUT_DEVICE
    sd.default.samplerate = parameters.SAMPLING_FREQUENCY
    mido.set_backend('mido.backends.pygame')
