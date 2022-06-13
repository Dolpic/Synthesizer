from multiprocessing import Queue, Process
from parameters import *
from Synthesizer import *
from GUI import *
from utils import *

if __name__ == "__main__":
    queue = Queue()
    synth = Synthesizer(queue)
    gui = GUI(queue)
    proc = Process(target=gui.run).start()
    show_peripherals()
    synth.run()
