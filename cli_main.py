from Synthesizer import Synthesizer
from FilePlayer import FilePlayer
from GUI import GUI

from utils import show_peripherals
import current_script

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

    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    sd.default.device = parameters.OUTPUT_DEVICE
    sd.default.samplerate = parameters.SAMPLING_FREQUENCY
    midi_input = pygame.midi.Input(parameters.INPUT_MIDI_DEVICE)
    pygame.midi.init()
    mido.set_backend('mido.backends.pygame')

    if args["m"]:
        file_player = FilePlayer(args["m"])
        file_player_proc = Process(target=file_player.run)

    queue = Queue()
    synth = Synthesizer(queue, midi_input)
    gui = GUI(queue)
    proc = Process(target=gui.run).start()
    show_peripherals()

    if args["m"]:
        file_player_proc.start()

    synth.run()
