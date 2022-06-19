"""This is the default script file, with type hints to make it easy to understand.
If you intend to make a custom script, it must provide the two classes below, each with its process() method with the given arguments."""

import MIDI.constants
import MIDI.filters.Default

import Modules.ADSR
import Modules.Linear
import Modules.Exponential
import Modules.Oscillators

import Modules.filters.Biquad.Notch
import Modules.filters.Biquad.PeakingEQ
import Modules.filters.Biquad.LowShelf
import Modules.filters.Biquad.LowPass
import Modules.filters.Biquad.BandPass
import Modules.filters.Biquad.HighPass
import Modules.filters.Distortion.Clip
import Modules.filters.Reverb
import Modules.filters.Resonator

import numpy as np
import parameters
import time

from typing import Optional, Tuple, NewType
from numpy.typing import NDArray

# Midi Types
MidiKey = NewType("MidiKey", int)
MidiStatusCode = NewType("MidiStatusCode", int)
NormalizedMidiVelocity = NewType("NormalizedMidiVelocity", float)

# Pure Audio Types
Frequency = NewType("Frequency", float)
Amplitude = NewType("Amplitude", float)

# DSP Types
SampleIndex = NewType("SampleIndex", int)
RightChannelSampleValue = NewType("RightChannelSampleValue", float)
LeftChannelSampleValue = NewType("LeftChannelSampleValue", float)


class MidiToFreq:
    def __init__(self):
        self.filter = MIDI.filters.Default.Default()

    def process(
        self,
        status: Optional[MidiStatusCode],
        key: Optional[MidiKey],
        velocity_0_to_1: Optional[NormalizedMidiVelocity],
    ) -> NDArray[Tuple[Frequency, Amplitude]]:
        return self.filter.process(status, key, velocity_0_to_1)


class FreqToAudio:
    def __init__(self):
        # Oscillators
        self.sine = Modules.Oscillators.Sine()

        # ADSR
        attack_time = 0.05
        attack_stop_level = 0.8
        attack_func = Modules.Linear.Linear(start=0, stop=attack_stop_level, duration=attack_time)
        decay_time = attack_time
        decay_func=Modules.Linear.Linear(start=attack_stop_level, stop=0.7, duration=decay_time)
        release_time = 0.05
        release_func = Modules.Linear.Linear(attack_stop_level, 0, release_time)
        self.adsr = Modules.ADSR.ADSR(
            attack_time=attack_time, attack_func=attack_func,
            decay_time=decay_time,   decay_func=decay_func,
            sustain_func=0.7,
            release_time=release_time, release_func=release_func,
        )

    def process(self, indexes, freqs_amps):
        output = np.zeros(parameters.SAMPLES_PER_FRAME)
        
        # There is no filtering of frequencies and amplitudes in this example
        freqs_amps = self.adsr.get(indexes, freqs_amps)

        # Oscillators
        for freq, amp in freqs_amps:
            # Security cutting frequencies over the Nyquist frequency
            if freq > parameters.NYQUIST_FREQUENCY: continue
            output += self.sine.set(freq, amp=amp).get(indexes, output)
            
        # There is no filtering of audio signal in this example
        
        # This example is mono
        return output, output 