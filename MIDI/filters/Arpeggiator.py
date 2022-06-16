import time
from MIDI.constants import MIDI_UP, MIDI_DOWN
from MIDI.utils import is_piano_key


class Arpeggiator:
    def __init__(self):
        self.schedule_list = []
        self.repeat = True
        self.arpege = [(0, 0.2, 0), (5, 0.2, -0.1), (9, 0.2, -0.3)]

    def process(self, status, note, velocity):
        if is_piano_key(note):
            if status == MIDI_DOWN:
                self.schedule(note, velocity)
            elif status == MIDI_UP:
                self.unschedule(note)
        return self.get_notes()

    def get_notes(self):
        output = []
        for (note, vel), (step, goal_time, goal_note, goal_vel) in self.schedule_list:
            output.append((goal_note, goal_vel))
            if time.time() >= goal_time:
                self.unschedule(note)
                self.schedule(note, vel, (step + 1) % len(self.arpege))
        return output

    def schedule(self, note, velocity, step=0):
        shift_note, shift_time, shift_veloctiy = self.arpege[step]
        next_time = time.time() + shift_time
        next_note = note + shift_note
        next_vel = velocity + shift_veloctiy
        self.schedule_list.append(
            ((note, velocity), (step, next_time, next_note, next_vel))
        )

    def unschedule(self, note):
        self.schedule_list = list(filter(lambda x: x[0][0] != note, self.schedule_list))
