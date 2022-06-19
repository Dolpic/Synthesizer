import os
import numpy as np
import sounddevice as sd
from pynput.keyboard import Key, Listener

import parameters
import current_script

from MIDI.MidiHandler import MidiHandler


class Synthesizer:
    def __init__(self, queue, midi_input_device, jupyter_mode=True, file_player_proc=None):
        self.queue = queue
        self.is_running = True
        self.midi_input = midi_input_device
        self.jupyter_mode = False
        self.file_player_proc = file_player_proc

    def run(self):
        if self.jupyter_mode:
            Listener(on_press=self.on_press).start()
        else:
            self.is_running = True
            self.file_player_proc.start()

        midi_handler = MidiHandler()
        audio_stream = sd.OutputStream(channels=2)
        audio_stream.start()
        current_sample = 0

        while self.is_running:
            indexes = np.arange(
                current_sample, current_sample + parameters.SAMPLES_PER_FRAME
            )

            freq_amp = midi_handler.process(self.midi_input)

            right_samples, left_samples = current_script.freqtoaudio.process(
                indexes, freq_amp
            )

            right_samples = right_samples.astype("float32") * parameters.GENERAL_VOLUME
            left_samples = left_samples.astype("float32") * parameters.GENERAL_VOLUME

            self.queue.put_nowait(left_samples)  # For the FFT GUI.

            audio_stream.write(np.column_stack((right_samples, left_samples)))
            current_sample += parameters.SAMPLES_PER_FRAME

        audio_stream.stop()

    def on_press(self, key):
        if key == Key.enter:
            self.is_running = False
