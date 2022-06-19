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
import Modules.filters.Comb

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
        # Filters
        self.reverb = Modules.filters.Reverb.Reverb(delay=0.005, dampening=0.25)
        self.lowpass = Modules.filters.Biquad.LowPass.LowPass(4200, 1.5)  # 4200 is just above the highest frequency a piano can do

        # Oscillators
        self.sine = Modules.Oscillators.Sine()

        # ADSR
        attack_time = 0.005
        attack_stop_level = 0.9
        attack_func = Modules.Linear.Linear(start=0, stop=attack_stop_level, duration=attack_time)
        decay_time = 3
        decay_func = Modules.Exponential.Exponential(start=attack_stop_level, stop=0, duration=decay_time)
        release_time = 0.2
        release_func = Modules.Linear.Linear(attack_stop_level, 0, release_time)
        self.adsr = Modules.ADSR.ADSR(
            attack_time=attack_time, attack_func=attack_func,
            decay_time=decay_time,   decay_func=decay_func,
            sustain_func=0,
            release_time=release_time, release_func=release_func,
        )

    def process(
        self,
        indexes: NDArray[SampleIndex],
        freqs_amps: NDArray[Tuple[Frequency, Amplitude]],
    ) -> Tuple[NDArray[RightChannelSampleValue], NDArray[LeftChannelSampleValue]]:
        output = np.zeros(parameters.SAMPLES_PER_FRAME)

        # Frequencies filtering - ADSR
        freqs_amps = self.adsr.get(indexes, freqs_amps)

        # Oscillators
        # overtones taken from a C4 on a piano, but slightly modified
        # the tuples are [overtone_number, amplitude]
        overtones = [
            [0.25, 0.2],
            [0.5, 0.2],
            [1, 1],
            [2, 0.9],
            # [3, 0.15],
            [4, 0.39],
            [5, 0.39],
            # [6, 0.05],
            # [7, 0.05],
            # [9, 0.05]
        ]
        for freq, amp in freqs_amps:
            for over_mult, over_amp in overtones:
                output += self.sine.set(freq*over_mult, amp=amp*over_amp).get(indexes, output)

        # Audio filtering
        output = self.lowpass.get(indexes, output)
