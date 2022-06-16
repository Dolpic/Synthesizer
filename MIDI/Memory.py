
class Memory:
    def __init__(self, size=2):
        self.cells = []
        self.size = size

    def add(self, freq, amplitude, note):
        if len(self.cells) >= self.size:
            self.cells = [[freq, amplitude, note]] + self.cells[:-1]
        else:
            self.cells = [[freq, amplitude, note]] + self.cells

    def contains(self, freq, amplitude, note):
        for f, a, n in self.cells:
            if freq == f and amplitude == a and note == n:
                return True
        return False
