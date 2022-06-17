import os
import numpy as np
import sounddevice as sd

import parameters
import current_script

from MIDI.MidiHandler import MidiHandler

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.midi  # noqa:E402


class Synthesizer:
    def __init__(self, queue):
        sd.default.device = parameters.OUTPUT_DEVICE
        sd.default.samplerate = parameters.SAMPLING_FREQUENCY
        self.queue = queue

    def run(self):
        input_device = pygame.midi.Input(parameters.INPUT_MIDI_DEVICE)
        midi_handler = MidiHandler()
        audio_stream = sd.OutputStream(channels=2)
        audio_stream.start()
        is_running = True
        current_sample = 0

        while is_running:
            indexes = np.arange(current_sample, current_sample + parameters.SAMPLES_PER_FRAME)

            freq_amp = midi_handler.process(input_device)

            right_samples, left_samples = current_script.freqtoaudio.process(indexes, freq_amp)

            right_samples = right_samples.astype("float32") * parameters.GENERAL_VOLUME
            left_samples = left_samples.astype("float32") * parameters.GENERAL_VOLUME

            self.queue.put_nowait(left_samples)  # For the FFT GUI.

            audio_stream.write(np.column_stack((right_samples, left_samples)))
            current_sample += parameters.SAMPLES_PER_FRAME
