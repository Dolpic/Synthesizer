import pygame.midi
import numpy as np
import sounddevice as sd

from parameters import INPUT_MIDI_DEVICE, GENERAL_VOLUME, OUTPUT_DEVICE, SAMPLING_FREQUENCY, SAMPLES_PER_FRAME
from MIDI.MidiHandler import MidiHandler
from Modules.Oscillators import Sine, Square, Sawtooth
from Modules.Filters.Biquad.LowPass import LowPass
from Modules.Filters.Biquad.HighPass import HighPass
from Modules.Filters.Reverb import *
from Modules.ADSR import *
from Modules.Linear import *
from Modules.Filters.Distortion.Clip import *

class Synthesizer:
    def __init__(self, queue):
        pygame.midi.init()
        sd.default.device = OUTPUT_DEVICE
        sd.default.samplerate = SAMPLING_FREQUENCY
        self.queue = queue

        self.lowPass = LowPass(1500, 3)
        self.highPass = HighPass(500, 3)
        self.reverb = Reverb(0.4, 0.7)

        self.clip = Clip(Sine(1,1,1), hardness=0)

        self.sine = Sine()
        self.square = Square()
        self.saw = Sine()

        self.adsr = ADSR(
            0.3, Linear(0 , 1  , 0.3), 
            0.3, Linear(1 , 0.2, 0.3), 
            0.2, 
            0.2, Linear(0.2 , 0, 0.2)
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
            times = np.arange(current_sample, current_sample+SAMPLES_PER_FRAME) / SAMPLING_FREQUENCY
            frequencies = midi_handler.process(input_device)

            # t1 = time.time()
            right, left = self.frequencies_to_sound(times, frequencies)
            # t2 = time.time()
            # ~0.0001s
            audio_stream.write(np.column_stack((right, left)))
            current_sample += SAMPLES_PER_FRAME

            # t3 = time.time()
            # print("Max : ", round(SAMPLES_PER_FRAME/SAMPLING_FREQUENCY,5), "sum:",round(t3-t0,5), " | 0-1:",  round(t1-t0,5), "1-2:",round(t2-t1,5),"2-3",round(t3-t2,5))

    def frequencies_to_sound(self, times, frequencies):
        outputs = np.zeros(len(times))

        #frequencies = self.adsr.get(frequencies)

        # Time : 1e-06
        for freq, amp in frequencies:
            outputs += self.sine.set(freq, amp=1).get(times)
            #outputs += self.square.set(freq*2, amp=amp/2).get(times)
            #outputs += self.saw.set(freq*3, amp=amp/3).get(times)

        #outputs = self.lowPass.get(outputs)
        #outputs = self.highPass.get(outputs)
        outputs = self.clip.get(outputs)
        #outputs = self.reverb.get(outputs)

        outputs = outputs.astype('float32') * GENERAL_VOLUME*0.5
        self.queue.put_nowait(outputs)
        return outputs, outputs
