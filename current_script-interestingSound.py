"""This is the default script file, with type hints to make it easy to understand."""

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

import numpy
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
LeftChannelSampleValue = NewType("RightChannelSampleValue", float)


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
        self.lowPass = Modules.filters.Biquad.LowPass.LowPass(1500, 3)
        self.highPass = Modules.filters.Biquad.HighPass.HighPass(500, 3)

        self.reverb = Modules.filters.Reverb.Reverb(0.01, 0.2)

        self.clip = Modules.filters.Distortion.Clip.Clip(
            Modules.Oscillators.Sine(0.5, 0.2, 1)
        )

        # Oscillators
        self.sine = Modules.Oscillators.Sine()
        self.square = Modules.Oscillators.Square()
        self.saw = Modules.Oscillators.Sawtooth()

        # ADSR
        a_level = 0.9
        a_time = 0.01
        d_time = 1.5
        self.adsr = Modules.ADSR.ADSR(
            attack_time=a_time,
            attack_func=Modules.Linear.Linear(0.0, a_level, a_time),
            decay_time=d_time,
            decay_func=Modules.Exponential.Exponential(a_level, 0, d_time),
            sustain_func=0,
            release_time=0,
            release_func=0,
        )

        self.resonator = Modules.filters.Resonator.Resonator(0.4, freq_add=7, max=10)

    def process(
        self,
        sample_indexes_to_fill: NDArray[SampleIndex],
        freqs_to_play: NDArray[Tuple[Frequency, Amplitude]],
    ) -> Tuple[NDArray[RightChannelSampleValue], NDArray[LeftChannelSampleValue]]:

        filled_samples = numpy.zeros(len(sample_indexes_to_fill))

        freqs_to_play = self.resonator.get(sample_indexes_to_fill, freqs_to_play)
        freqs_to_play = self.adsr.get(sample_indexes_to_fill, freqs_to_play)

        for freq, amp in freqs_to_play:
            if freq > parameters.NYQUIST_FREQUENCY: continue
            filled_samples += self.saw.set(freq, amp=amp).get(sample_indexes_to_fill, filled_samples)
            filled_samples += self.sine.set(freq*2, amp=amp/2).get(sample_indexes_to_fill, filled_samples)
            filled_samples += self.sine.set(freq*3, amp=amp/2).get(sample_indexes_to_fill, filled_samples)
            #filled_samples += self.saw.set(freq * 3, amp=amp / 3).get(sample_indexes_to_fill, filled_samples)

        filled_samples = self.lowPass.get(sample_indexes_to_fill, filled_samples)
        #filled_samples = self.highPass.get(sample_indexes_to_fill, filled_samples)
        filled_samples = self.reverb.get(sample_indexes_to_fill, filled_samples)

        return filled_samples, filled_samples  # This example is mono...