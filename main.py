from multiprocessing import Queue, Process
from parameters import *
from Synthesizer import *
from GUI import *

if __name__ == "__main__":
    queue = Queue()
    synth = Synthesizer(queue)
    gui = GUI(queue)
    proc = Process(target=gui.run).start()
    synth.run()
