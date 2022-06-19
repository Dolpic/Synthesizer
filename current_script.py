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
        # Oscillators
        self.square = Modules.Oscillators.Square()
        self.white = Modules.Oscillators.WhiteNoise()
        self.comb = Modules.filters.Comb.Comb(1, 20)
        self.lowpass = Modules.filters.Biquad.LowPass.LowPass(10000, 2)
        self.lowpass_hard = Modules.filters.Biquad.LowPass.LowPass(6000, 2)
        self.clip = Modules.filters.Distortion.Clip.Clip(1.5, 0.2)
        self.reverb = Modules.filters.Reverb.Reverb(0.01, 0.4)
        self.lfo = Modules.Oscillators.Sine(4, 0.05)

        # ADSR
        attack_time = 0.07
        attack_stop_level = 0.8
        attack_func = Modules.Linear.Linear(
            start=0, stop=attack_stop_level, duration=attack_time
        )
        decay_time = attack_time
        decay_func = Modules.Linear.Linear(
            start=attack_stop_level, stop=0.7, duration=decay_time
        )
        release_time = 0.1
        release_func = Modules.Linear.Linear(attack_stop_level, 0, release_time)
        self.adsr = Modules.ADSR.ADSR(
            attack_time=attack_time,
            attack_func=attack_func,
            decay_time=decay_time,
            decay_func=decay_func,
            sustain_func=0.7,
            release_time=release_time,
            release_func=release_func,
        )

    def process(
        self,
        indexes: NDArray[SampleIndex],
        freqs_amps: NDArray[Tuple[Frequency, Amplitude]],
    ) -> Tuple[NDArray[RightChannelSampleValue], NDArray[LeftChannelSampleValue]]:
        output = np.zeros(parameters.SAMPLES_PER_FRAME)

        freqs_amps = self.adsr.get(indexes, freqs_amps)

        # Oscillators
        for freq, amp in freqs_amps:
            # Security cutting frequencies over the Nyquist frequency
            if freq > parameters.NYQUIST_FREQUENCY: continue
            output += self.white.get(indexes, output) * amp/5
            output += self.square.set(freq,amp+self.lfo.get(indexes, output)).get(indexes, output)

        output = self.comb.get(indexes, output)

        output_reverb = self.lowpass_hard.get(indexes, output)
        output_reverb = self.reverb.get(indexes, output_reverb)
        output = 0.5*output + 0.5*output_reverb

        output = self.lowpass.get(indexes, output)



        return output, output
