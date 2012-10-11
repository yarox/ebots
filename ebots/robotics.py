from __future__ import division

import threading
import morsesim
import time


class RoboticsError(Exception):
    pass


class IntervalRunner(threading.Thread):
    def __init__(self, interval, steps, func, *args, **kwargs):
        self.interval = interval
        self.steps = steps
        self.func = func

        self.kwargs = kwargs
        self.args = args

        super(IntervalRunner, self).__init__()

    def run(self):
        for i in range(self.steps):
            self.func(*self.args, **self.kwargs)
            time.sleep(self.interval)


class BaseRobot(object):
    def __init__(self, components, name='dummy'):
        self.actuators = []
        self.sensors = []
        self.name = name

        self._create_devices(components)

    def _create_devices(self, components):
        for name, port in sorted(components.items()):
            kind, id = name.split('_')
            device = getattr(morsesim, kind.title())

            if device is morsesim.Actuator:
                self.actuators.append(device(name, port))
            elif device is morsesim.Sensor:
                self.sensors.append(device(name, port))
            else:
                msg = 'device {0} does not exists'.format(device)
                raise RoboticsError(msg)

    def _execute(self):
        '''
        Base clases must implement this method.
        '''
        pass

    def move(self, steps, interval):
        thread = IntervalRunner(interval, steps, self._execute)
        thread.start()


class NeuralRobot(BaseRobot):
    def __init__(self, components, network, name='dummy'):
        self.network = network
        super(NeuralRobot, self).__init__(components, name)


class ValentinoRobot(NeuralRobot):
    def _execute(self):
        input = [min(sensor.read()['range_list']) for sensor in self.sensors]
        out0, out1 = self.network.eval(input)

        velocity = (out0 + out1) / 2
        omega = (out0 - out1)

        actuator = self.actuators[0]
        actuator.write({'v': velocity, 'w': omega})

        print(actuator.name, velocity, omega)
