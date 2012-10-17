from __future__ import division
from collections import defaultdict

import morsesim
import time


class RoboticsError(Exception):
    pass


class BaseRobot(object):
    def __init__(self, components, name='dummy', host='localhost'):
        self.components = components

        self.actuators = defaultdict(list)
        self.sensors = defaultdict(list)
        self.name = name
        self.host = host

        self._create_devices(components)

    def _create_devices(self, components):
        for name, port in sorted(components.items()):
            kind, type, did, rid = name.split('_')
            device = getattr(morsesim, kind.title())

            if device is morsesim.Actuator:
                self.actuators[type].append(device(name, port, self.host))
            elif device is morsesim.Sensor:
                self.sensors[type].append(device(name, port, self.host))
            else:
                msg = 'device {0} does not exists'.format(device)
                raise RoboticsError(msg)


class NeuralRobot(BaseRobot):
    def __init__(self, components, network, name='dummy', host='localhost'):
        self.network = network
        super(NeuralRobot, self).__init__(components, name, host)


class EnergyRobot(NeuralRobot):
    def __init__(self, components, network, name='dummy', host='localhost'):
        self.cookies = {}
        self.energy = 0
        super(self.__class__, self).__init__(components, network, name, host)

    def move(self, steps, interval):
        self.cookies = {}
        self.energy = 0

        proximity = self.sensors['proximity'][0]
        waypoint = self.actuators['waypoint'][0]
        motion = self.actuators['motion'][0]
        rangers = self.sensors['ranger']

        for i in range(steps + 30):
            input = [min(ranger.read()['range_list']) for ranger in rangers]
            velocity, omega = self.network.eval(input)

            if i < 30:
                motion.write({'v': 0, 'w': 0})
                waypoint.write({'x': 0, 'y': 0, 'z': 0, 'tolerance': 0.5, 'speed': 5})

            else:
                cookies = proximity.read()['near_objects']
                if set(cookies).difference(set(self.cookies)):
                    self.energy += 1
                self.cookies.update(cookies)

                waypoint.write({'x': 0, 'y': 0, 'z': 0, 'tolerance': 0.5, 'speed': 0})
                motion.write({'v': velocity, 'w': omega})

            time.sleep(interval)
            #print(motion.name, velocity, omega, self.energy)
