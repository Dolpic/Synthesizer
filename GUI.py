import tkinter as tk
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure 
from scipy.fft import rfft

from parameters import *

class GUI:
    def __init__(self, queue):
        self.window = tk.Tk()
        fig = Figure() 
        self.ax = fig.add_subplot(211) 
        self.ax2 = fig.add_subplot(212) 
        self.ax.set_ylim(-200, 0)
        #self.ax.get_yaxis().set_visible(False)
        #self.ax.set_xscale('log')
        #self.ax.set_xlim(20, 20000)

        self.graph = FigureCanvasTkAgg(fig, master=self.window) 
        self.graph.get_tk_widget().pack(side="top",fill='both',expand=True)
        self.queue = queue

    def run(self):
        self.update_window()
        self.window.mainloop()

    def update_window(self):
        signal = np.empty(0)

        while not self.queue.empty() :
            signal = np.concatenate((signal, self.queue.get()))

        if len(signal) > 0 :
            signal = np.where(signal == 0, 1e-15, signal)
            _,_,serie = self.ax.magnitude_spectrum(signal, Fs=SAMPLING_FREQUENCY, scale="dB", color="black")
            _,_,serie2 = self.ax2.magnitude_spectrum(signal, Fs=SAMPLING_FREQUENCY, scale="linear", color="black")
            self.graph.draw()
            serie.remove()
            serie2.remove()

        self.window.after(int(1000/WINDOW_REFRESH_RATE), self.update_window)