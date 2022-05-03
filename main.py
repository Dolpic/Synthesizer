import pygame.midi
import numpy as np
import sounddevice as sd
import threading
from scipy import signal

pygame.midi.quit()
pygame.midi.init()

DEBUG = True
SAMPLING_FREQUENCY = 44100 
NB_SAMPLES_PER_FRAME = 1024

def run():
    is_running = True

    while is_running:

        frame_times = np.arange(current_sample, current_sample+self.NB_SAMPLES_PER_FRAME)
        times = frame_times / self.DEFAULT_SF
            
            waves = []

            for i in range(len(self.frequencies)):
                tmp = Wave.sin(times, self.frequencies[i])
                waves.append(tmp)

            w = []
            if len(self.frequencies) != 0 : w = sum(waves)/len(self.frequencies)

            if input_device.poll():
                event = input_device.read(1)[0]
                self.midiHandler(status=event[0][0], note=event[0][1], vel=event[0][2])
                if self.debug : print(f"status:{event[0][0]}, note:{event[0][1]}, velocity:{event[0][2]}, timestamp:{event[1]}") 
                
        self.audio_stream.write(np.column_stack( (w,w) ).astype('float32'))
        current_sample += self.NB_SAMPLES_PER_FRAME

run()

