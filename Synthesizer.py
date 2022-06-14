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
from Modules.Oscillators import Sine, Square, Sawtooth
from Modules.Filters.Biquad.LowPass import LowPass
from Modules.Filters.Biquad.HighPass import HighPass
from Modules.Filters.Reverb import Reverb
from Modules.ADSR import ADSR
from Modules.Linear import Linear


class Synthesizer:
    def __init__(self, queue):
        pygame.midi.init()
        sd.default.device = OUTPUT_DEVICE
        sd.default.samplerate = SAMPLING_FREQUENCY
        self.queue = queue

        self.lowPass = LowPass(15000, 3)
        self.highPass = HighPass(50, 3)
        self.reverb = Reverb(0.05, 0.7)

        self.sine = Sine()
        self.square = Square()
        self.saw = Sawtooth()

        a_level = 0.9
        a = 0.1
        d = 0.05
        s = 0.8
        r = 0.05
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
            times = (
                np.arange(current_sample, current_sample + SAMPLES_PER_FRAME)
                / SAMPLING_FREQUENCY
            )
            frequencies_amplitudes = midi_handler.process(input_device)

            # t1 = time.time()
            right, left = self.frequencies_to_sound(times, frequencies_amplitudes)
            # t2 = time.time()
            # ~0.0001s
            audio_stream.write(np.column_stack((right, left)))
            current_sample += SAMPLES_PER_FRAME

            # t3 = time.time()
            # print("Max : ", round(SAMPLES_PER_FRAME/SAMPLING_FREQUENCY,5), "sum:",round(t3-t0,5), " | 0-1:",  round(t1-t0,5), "1-2:",round(t2-t1,5),"2-3",round(t3-t2,5))

    def frequencies_to_sound(self, times, frequencies_amplitudes):
        outputs = np.zeros(len(times))

        frequencies_amplitudes = self.adsr.get(frequencies_amplitudes)

        # Time : 1e-06
        for freq, amp in frequencies_amplitudes:
            outputs += self.sine.set(freq, amp=amp).get(times)
            # outputs += self.square.set(freq*2, amp=amp/2).get(times)
            outputs += self.saw.set(freq * 3, amp=amp / 4).get(times)

        outputs = self.lowPass.get(outputs)
        outputs = self.highPass.get(outputs)
        # outputs = self.reverb.get(outputs)

        outputs = outputs.astype("float32") * GENERAL_VOLUME
        self.queue.put_nowait(outputs)
        return outputs, outputs
