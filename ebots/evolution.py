import random


class DifferentialEvolution(object):
    def __init__(self, F, CR, NP, Creator, *args, **kwargs):
        self.F = F
        self.CR = CR
        self.NP = NP

        self.Creator = Creator
        self.args = args
        self.kwargs = kwargs

        self.current = [Creator(*args, **kwargs) for i in range(NP)]
        self.candidates = [None for i in range(NP)]

        self.dimension = len(self.current[0])

    def recombine(self):
        self.candidates = []

        for x in self.current:
            a, b, c = random.sample(self.current, 3)
            y = self.Creator(*self.args, **self.kwargs)

            R = random.randint(0, self.dimension + 1)

            for i in range(self.dimension):
                if (random.uniform(0, 1) < self.CR) or (i == R):
                    y[i] = a[i] + self.F * (b[i] - c[i])
                else:
                    y[i] = x[i]

            self.candidates.append(y)

    def select(self):
        self.current = [max(current, candidate) for current, candidate in
                        zip(self.current, self.candidates)]

    def __getitem__(self, key):
        return self.current[key], self.candidates[key]
