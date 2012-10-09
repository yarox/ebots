import morsesim
import robotics
import neural
import numpy


components = morsesim.get_components('morse-config')
network_config = [2, 2]
interval = 0.01
steps = 150

robots = []
for i, block in enumerate(components):
    network = neural.EvolvableFFANN(network_config, numpy.tanh)
    robot = robotics.ATRVRobot(block, network, 'robot_{0}'.format(i))
    robots.append(robot)

    print('{0} is ready!'.format(robot.name))

for robot in robots:
    robot.move(steps, interval)
