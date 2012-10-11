import random


class DifferentialEvolution(object):
    def __init__(self, F, CR, NP):
        self.F = F
        self.CR = CR
        self.NP = NP

        self.population = []
        self.dimension = None

    def create_population(self, Creator, kwargs):
        self.Creator = Creator
        self.kwargs = kwargs

        for i in range(self.NP):
            self.population.append(Creator(**kwargs))

        self.dimension = len(self.population[0])

    def recombine(self):
        self.candidates = []

        for x in self.population:
            a, b, c = random.sample(self.population, 3)
            y = self.Creator(self.kwargs)

            R = random.randint(0, self.NP - 1)

            for i in range(self.dimension):
                if (random.uniform(0, 1) < self.CR) or (i == R):
                    y[i] = a[i] + self.F * (b[i] - c[i])
                else:
                    y[i] = x[i]

            self.candidates.append(y)

    def evaluate(self):
        pass

    def run(self, steps):
        pass
