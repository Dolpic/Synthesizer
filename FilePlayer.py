import mido
import time
import pygame.midi

import parameters


class FilePlayer:
    def __init__(self, path):
        self.midi = mido.MidiFile(path)

    def run(self):
        time.sleep(1)

        port_name = pygame.midi.get_device_info(parameters.INPUT_MIDI_DEVICE)[1].decode()
        port = mido.open_output(port_name)
        for msg in self.midi.play():
            port.send(msg)
