import numpy as np
from parameters import *

class MidiHandler:

    keys_down = {}
    result = ([], [])

    amplitudes = np.empty(0)
    notes = np.empty(0)

    def handle(self, input):

        if input.poll():
            status, note, velocity, _ = input.read(1)[0][0]
            if DEBUG :
                print(f"status:{status}, note:{note}, velocity:{velocity}") 
                
        # Tools
        #if status == 176:
        #    if note == 114:
        #        self.stop()
        #    elif note >=22 and note <= 29:
        #        ...

            # Notes
            if note >= MIDI_LOWER_KEY and note <= MIDI_HIGHER_KEY :
                if status == MIDI_DOWN:
                    self.keys_down[note] = velocity
                elif status == MIDI_UP:
                    self.keys_down.pop(note)

            self.amplitudes = np.asarray(list(self.keys_down.values())  , dtype='float32')/127
            self.notes      = np.asarray(list(self.keys_down.keys()), dtype='float32')

        return np.column_stack( (self.midi_to_frequency(self.notes), self.amplitudes) )


    def midi_to_frequency(self, midi_number):
        REF_NOTE = 69
        REF_FREQUENCY = 440
        NB_NOTES_IN_SCALE = 12
        OCTAVE_FREQUENCY_RATIO = 2
        return np.power(OCTAVE_FREQUENCY_RATIO, (midi_number-REF_NOTE)/NB_NOTES_IN_SCALE )*REF_FREQUENCY

        
    """
    def amp(x, force):
        result = []
        for sample in x:result.append(sample*force)  
        return result  
    
    def get_harmoniques(frequency):
        return [frequency*2, frequency*3, frequency*4, frequency*5, frequency*6, frequency*7, frequency*8, frequency*9]
    """

        