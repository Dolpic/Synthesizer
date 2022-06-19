import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from Synthesizer import Synthesizer
from FilePlayer import FilePlayer
from GUI import GUI

import utils
import current_script

import parameters
import pygame.midi
import mido
import argparse
from multiprocessing import Queue, Process
import sounddevice as sd

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Synthesize some sounds with a script (or not).")
    parser.add_argument("-s", type=str, default=None, metavar="SCRIPT", help="A script to customize the synthesis. Refer to current_script.py for an example.")
    parser.add_argument("-m", type=str, default=None, metavar="MIDI_FILE", help="A midi file to play along with you.")
    args = vars(parser.parse_args())

    # Allow customization of the script
    if args["s"]:
        with open(args["s"], "r") as script:
            exec(script.read(), globals())
            try:
                current_script.MidiToFreq = MidiToFreq  # should be defined from the executed script.
                current_script.FreqToAudio = FreqToAudio  # same
            except NameError:
                raise ValueError("If you supply a script, please define classes MidiToFreq and FreqToAudio.")

    current_script.miditofreq = current_script.MidiToFreq()
    current_script.freqtoaudio = current_script.FreqToAudio()

    utils.init()
    pygame.midi.init()
    midi_input = pygame.midi.Input(parameters.INPUT_MIDI_DEVICE)

    queue = Queue()
    gui = GUI(queue)
    proc = Process(target=gui.run).start()
    synth = Synthesizer(queue, midi_input)
    synth.run()

    if args["m"]:
        file_player = FilePlayer(args["m"])
        file_player_proc = Process(target=file_player.run)
        file_player_proc.start()
