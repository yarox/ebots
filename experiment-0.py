from ebots import morsesim, neural, robotics
from numpy import tanh


components = morsesim.get_components('morse-config')
network_config = [2, 2]
interval = 0.01
steps = 150

robots = []
for i, block in enumerate(components):
    network = neural.EvolvableFFANN(network_config, tanh)
    robot = robotics.ValentinoRobot(block, network, 'robot_{0}'.format(i), '192.168.1.11')
    robots.append(robot)

    print('{0} is ready!'.format(robot.name))

for robot in robots:
    robot.move(steps, interval)
