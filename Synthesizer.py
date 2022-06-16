import pygame.midi
import numpy as np
import sounddevice as sd

from parameters import (
    INPUT_MIDI_DEVICE,
    GENERAL_VOLUME,
    OUTPUT_DEVICE,
    SAMPLING_FREQUENCY,
    SAMPLES_PER_FRAME,
)
from MIDI.MidiHandler import MidiHandler
from Modules.Oscillators import Sine, Square, Sawtooth, WhiteNoise
from Modules.Filters.Biquad.LowPass import LowPass
from Modules.Filters.Biquad.HighPass import HighPass
from Modules.Filters.Reverb import Reverb
from Modules.ADSR import ADSR
from Modules.Linear import Linear
from Modules.Filters.Distortion.Clip import *
from Modules.Filters.Resonator import *


class Synthesizer:
    def __init__(self, queue):
        pygame.midi.init()
        sd.default.device = OUTPUT_DEVICE
        sd.default.samplerate = SAMPLING_FREQUENCY
        self.queue = queue

        self.lowPass = LowPass(Sine(2, 1100, 1500), 3)
        self.highPass = HighPass(500, 3)
        self.reverb = Reverb(0.05, 0.4)

        #self.clip = Clip(Sine(0.5, 1, 1.5))
        #self.clip = Clip(0.5)

        self.resonator = Resonator(1/3, 0.5)

        self.sine = Sine()
        self.square = Square()
        self.saw = Sine()

        self.white = WhiteNoise()

        a_level = 0.9
        a = 3
        d = 0.05
        s = 0.8
        r = 0.4
        self.adsr = ADSR(
            attack_time=a,
            attack_func=Linear(0.0, a_level, a),
            decay_time=d,
            decay_func=Linear(a_level, s, d),
            sustain_func=s,
            release_time=r,
            release_func=Linear(s, 0.0, r),
        )

    def run(self):
        input_device = pygame.midi.Input(INPUT_MIDI_DEVICE)
        midi_handler = MidiHandler()
        audio_stream = sd.OutputStream(channels=2)
        audio_stream.start()
        is_running = True
        current_sample = 0

        while is_running:
            # Time : 1e-04
            # t0 = time.time()
            indexes = np.arange(current_sample, current_sample + SAMPLES_PER_FRAME)
            freq_amp = midi_handler.process(input_device)

            # t1 = time.time()
            right, left = self.frequencies_to_sound(indexes, freq_amp)
            # t2 = time.time()
            # ~0.0001s
            audio_stream.write(np.column_stack((right, left)))
            current_sample += SAMPLES_PER_FRAME

            # t3 = time.time()
            # print("Max : ", round(SAMPLES_PER_FRAME/SAMPLING_FREQUENCY,5), "sum:",round(t3-t0,5), " | 0-1:",  round(t1-t0,5), "1-2:",round(t2-t1,5),"2-3",round(t3-t2,5))

    def frequencies_to_sound(self, indexes, freq_amp):
        outputs = np.zeros(len(indexes))

        #freq_amp = Resonator(0.7, freq_add=2, max=5).get(indexes, freq_amp)
        #freq_amp = self.adsr.get(indexes, freq_amp)

        # Time : 1e-06
        for freq, amp in freq_amp:
            if freq >= NYQUIST_FREQUENCY : continue # Prevent aliasing
            outputs += self.white.get(freq, amp)
            #outputs += self.sine.set(freq, amp=amp).get(indexes, outputs)
            #outputs += self.square.set(freq*2, amp=amp/2).get(indexes, outputs)
            #outputs += self.saw.set(freq*3, amp=amp/3).get(indexes, outputs)

        #outputs = self.lowPass.get(indexes, outputs)
        #outputs = self.highPass.get(indexes, outputs)
        #outputs = self.clip.get(indexes, outputs)
        #outputs = self.reverb.get(indexes, outputs)

        outputs = outputs.astype("float32") * GENERAL_VOLUME
        self.queue.put_nowait(outputs)
        return outputs, outputs
