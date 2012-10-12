from ebots import morsesim, neural, robotics, evolution
from numpy import tanh


components = morsesim.get_components('morse-config')

network_config = [2, 2]
interval = 0.01
steps = 150

F, CR, NP = 0.8, 0.9, 60
num_iterations = 100

robot = robotics.EnergyRobot(components[0], None, 'robot_0', '192.168.1.11')
population = evolution.DifferentialEvolution(F, CR, NP, neural.EvolvableFFANN,
             network_config, tanh)

for iteration in range(num_iterations):
    population.recombine()

    for individual in population:
        robot.network = individual
        robot.move(steps, interval)

    population.select()
