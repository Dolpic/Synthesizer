import time
from parameters import MIDI_DOWN, MIDI_UP
from MIDI.midi_utils import is_piano_key


class Envelope:

    def __init__(self, envelope_function, envelope_max_time):
        self.schedule_list = []
        self.envelope = envelope_function
        self.envelope_max_time = envelope_max_time

    def process(self, status, note, velocity):
        if is_piano_key(note):
            if status == MIDI_DOWN:
                self.schedule(note, velocity)
            elif status == MIDI_UP:
                self.unschedule(note)
        return self.get_notes()

    def get_notes(self):
        new_schedule_list = []
        now = time.time()
        output = []

        for (note, goal_vel, hit_time) in self.schedule_list:
            if now - hit_time < self.envelope_max_time:
                curr_vel = self.envelope(now - hit_time)
                output.append((note, curr_vel))
                new_schedule_list.append((note, goal_vel, hit_time))

        self.schedule_list = new_schedule_list

        return output

    def schedule(self, note, velocity):
        now = time.time()
        self.schedule_list.append((note, velocity, now))

    def unschedule(self, note):
        pass
