"""This is the default script file, with type hints to make it easy to understand.
If you intend to make a custom script, it must provide the two classes below, each with its process() method with the given arguments."""

import MIDI.constants
import MIDI.filters.Default

import Modules.ADSR
import Modules.Linear
import Modules.Exponential
import Modules.Oscillators

import Modules.filters.Biquad.LowPass
import Modules.filters.Biquad.HighPass
import Modules.filters.Distortion.Clip
import Modules.filters.Reverb
import Modules.filters.Resonator

import numpy as np
import parameters

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
        # Filters
        self.reverb = Modules.filters.Reverb.Reverb(delay=0.005, dampening=0.3)

        # Oscillators
        self.sine = Modules.Oscillators.Sine()

        # ADSR
        attack_time = 0.005
        attack_stop_level = 0.9
        attack_func = Modules.Linear.Linear(start=0, stop=attack_stop_level, duration=attack_time)
        decay_time = 3
        decay_func=Modules.Exponential.Exponential(start=attack_stop_level, stop=0, duration=decay_time)
        release_time = 0.1
        release_func = Modules.Linear.Linear(attack_stop_level, 0, release_time)
        self.adsr = Modules.ADSR.ADSR(
            attack_time=attack_time, attack_func=attack_func,
            decay_time=decay_time,   decay_func=decay_func,
            sustain_func=0,
            release_time=release_time, release_func=release_func,
        )

    def process(self, indexes, freqs_amps) :
        output = np.zeros(parameters.SAMPLES_PER_FRAME)

        # Frequencies filtering - ADSR
        freqs_amps = self.adsr.get(indexes, freqs_amps)

        # Oscillators
        overtones = [
            [1, 1],
            [2, 0.9],
            [3, 0.15],
            [4, 0.39],
            [5, 0.39],
            [6, 0.1],
            [7, 0.2],
            [9, 0.15]
        ]
        for freq, amp in freqs_amps:
            if freq > parameters.NYQUIST_FREQUENCY: continue
            for over_mult, over_amp in overtones:
                output += self.sine.set(freq*over_mult, amp=amp*over_amp).get(indexes, output)

        # Audio filtering
        output = self.reverb.get(indexes, output)

        return output, output
