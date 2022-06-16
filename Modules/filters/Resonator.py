from Modules.Module import Module

class Resonator(Module):
    audible_limit = 0.0001

    def __init__(self, dampening, freq_mult=1, freq_add=0, max=100000):
        super().__init__()
        (
            self.dampening,
            self.freq_mult,
            self.freq_add,
            self.max,
        ) = self._param_to_modules([dampening, freq_mult, freq_add, max])

    def get(self, indexes, freq_amp):
        result = []

        for freq, amp in freq_amp:
            initial_freq = freq
            count = 0
            while (
                amp > self.audible_limit and count <= self.max.get(indexes, indexes)[0]
            ):
                result.append([freq, amp])
                freq *= self.freq_mult.get(indexes, indexes)[0]
                freq += initial_freq * self.freq_add.get(indexes, indexes)[0]
                amp *= self.dampening.get(indexes, indexes)[0]
                count += 1

        return result
