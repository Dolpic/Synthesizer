from multiprocessing import Queue, Process
from Synthesizer import Synthesizer
from GUI import GUI
from utils import show_peripherals
import current_script

import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Synthesize some sounds with a script (or not).")
    parser.add_argument("-s", type=str, default=None)
    args = vars(parser.parse_args())

    # Allow customization
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

    queue = Queue()
    synth = Synthesizer(queue)
    gui = GUI(queue)
    proc = Process(target=gui.run).start()
    show_peripherals()
    synth.run()
