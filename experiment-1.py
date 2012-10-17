from ebots import morsesim, neural, robotics, evolution
from misc import generalized_logistic
from functools import partial
from pymongo import Connection
from numpy import mean


logistic = partial(generalized_logistic, A=-5, K=5, B=1, nu=0.5, Q=0.5, M=0.5)

collection = Connection()['experiment1']['take_one']
components = morsesim.get_components('morse-config')

interval, steps = 0.01, 100
iterations, trials = 20, 2
F, CR, NP = 0.8, 0.9, 20
network_config = [2, 2]

robot = robotics.EnergyRobot(components[0], None, 'robot_0', '127.0.0.1')
population = evolution.DifferentialEvolution(F, CR, NP,
             neural.EvolvableFFANN, network_config, logistic)

for iteration in range(iterations):
    population.recombine()
    info = []

    for i, (current, candidate) in enumerate(population):
        fitness = []
        robot.network = candidate

        for j in range(trials):
            robot.move(steps, interval)
            fitness.append(robot.energy)

        candidate.fitness = mean(fitness)

        msg = '> iteration {0}, individual {1}, fitness {2} (previous {3})'
        print msg.format(iteration, i, candidate.fitness, current.fitness)

        info.append({'iteration': iteration,
                     'robot': i,
                     'fitness': current.fitness,
                     'weights': current.weights})

    population.select()
    collection.insert(info)
