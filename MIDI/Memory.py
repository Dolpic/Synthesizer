from parameters import DEBUG


class Memory:
    def __init__(self, size=4):
        self.cells = []
        self.size = size

    def add(self, freq, amplitude, note):
        index = self.index(amplitude, note)

        if index < 0 : #if memory does not contains this note, add it.
            if len(self.cells) >= self.size:
                self.cells = [[freq, amplitude, note]] + self.cells[:-1]
            else:
                self.cells = [[freq, amplitude, note]] + self.cells
            if DEBUG:
                print("Added new value to memory. It now contains ", self.cells)

        else : #else, put it at index 0 to signify its importance
            self.cells = [[freq, amplitude, note]] + self.cells[:index] + self.cells[index+1:]

    def index(self, amplitude, note):
        result = 0
        for f, a, n in self.cells:
            if amplitude == a and note == n:
                return result
            result +=1
        return -1
