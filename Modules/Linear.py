from Modules.Module import Module


class Linear(Module):
    def __init__(self, start, stop, duration):
        super().__init__()
        self.start, self.stop, self.duration = self._param_to_modules(
            [start, stop, duration]
        )

    def get(self, input):
        times = self._get_next_times(len(input))
        b = self.start.get(input)
        a = (self.stop.get(input) - self.start.get(input)) / self.duration.get(input)
        return b + times * a
