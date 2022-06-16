import mido
import pygame.midi
import sounddevice as sd


def show_peripherals():
    print("PyGame MIDI Inputs : ")
    for i in range(pygame.midi.get_count()):
        (interf, name, input, output, opened) = pygame.midi.get_device_info(i)
        if input:
            print(
                "   {} : {} - {:<30}  Opened: {}".format(
                    i, interf.decode(), name.decode(), "yes" if opened else "no"
                )
            )
    print("\n")
    print("Mido MIDI Outputs : ")
    print(mido.get_output_names())
    print("\n")
    print("Audio Outputs : ")
    print(sd.query_devices())
