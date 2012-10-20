from pymongo import Connection
from itertools import groupby
from numpy import array, mean

import pylab


collection = Connection()['experiment1']['take_two']
mean_fitness = []
best_fitness = []
best_weights = []

for group, iteration in groupby(collection.find(), lambda x: x['iteration']):
    values = [(individual['fitness'], individual['weights'], i) for i, individual in enumerate(iteration)]
    fitness, weights, robots = zip(*values)

    _, best_robot = max(zip(fitness, robots))

    mean_fitness.append(mean(fitness))
    best_fitness.append(max(fitness))
    best_weights.append(array(weights[best_robot]))

fig, ax1 = pylab.subplots()

ax1.plot(range(1, 21), mean_fitness)
ax1.plot(range(1, 21), best_fitness)
ax1.axhline(32, ls='dashed')

ax1.set_ylim(0, 35)

ax1.set_xlabel('Iterations')
ax1.set_ylabel('Fitness')
ax1.set_title('Fitness Evolution')
ax1.legend(('Mean', 'Best', 'Max'), 'best')

fig.savefig('fitness_evo.png')
pylab.show()
