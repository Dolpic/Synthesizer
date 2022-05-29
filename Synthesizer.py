import pygame.midi
import numpy as np
import sounddevice as sd

from parameters import *
from utils import *
from MIDI.MidiHandler import MidiHandler
from Modules.Oscillators import *
from Modules.Filters.LowPass import *
from Modules.Filters.BandPass import *
from Modules.Filters.Reverb import *

class Synthesizer:
    def __init__(self, queue):
        pygame.midi.init()
        sd.default.device = OUTPUT_DEVICE
        self.queue = queue
        self.lowPass = LowPass(800, 0.8)
        self.bandPass = BandPass(600, 0.5)
        self.reverb = Reverb(0.01, 0.3)
        self.LFO = Sine(2, 1)

    def run(self):
        input_device = pygame.midi.Input(INPUT_MIDI_DEVICE)
        midi_handler = MidiHandler()
        audio_stream = sd.OutputStream(channels=2)
        audio_stream.start()
        is_running = True
        current_sample = 0

        while is_running:
            times = np.arange(current_sample, current_sample+SAMPLES_PER_FRAME) / SAMPLING_FREQUENCY
            frequencies = midi_handler.process(input_device)
            right, left = self.frequencies_to_sound(times, frequencies)    
            audio_stream.write(np.column_stack( (right, left) ).astype('float32'))
            current_sample += SAMPLES_PER_FRAME

    def frequencies_to_sound(self, times, frequencies):
        outputs = np.zeros(len(times))
        for freq, amp in frequencies:
            outputs += Sine(freq, amp).get(times)
            outputs += Square((freq)*2, 0.5, amp/2).get(times)
            outputs += Sawtooth((freq)*3, self.LFO.get(times)*amp/3).get(times)
        outputs *= GENERAL_VOLUME
        outputs = self.lowPass.process(outputs)
        #outputs = self.bandPass.process(outputs)
        outputs = self.reverb.process(outputs)
        self.queue.put_nowait(outputs)

        return outputs, outputs