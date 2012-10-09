from morse.builder.morsebuilder import *


num_robots = 8

for i in range(num_robots):
    devices = []

    robot = Robot('atrv')
    robot.name = 'robot_{0}'.format(i)
    robot.properties(Object=True, Label=robot.name)
    robot.translate(x=i, y=i, z=0.2)
    robot.rotate(z=i * 0.5)

    motion = Actuator('v_omega')
    motion.name = 'actuator_{0}'.format(i)
    devices.append(motion)

    sensorL = Sensor('sick-ld-mrs')
    sensorL.name = 'sensor_L{0}'.format(i)
    sensorL.translate(x=0.2, y=0.3, z=0.5)
    sensorL.rotate(z=0.523)
    sensorL.properties(Visible_arc=False, resolution=1, scan_window=60,
                       laser_range=5)
    sensorL.create_sick_arc()
    devices.append(sensorL)

    sensorR = Sensor('sick-ld-mrs')
    sensorR.name = 'sensor_R{0}'.format(i)
    sensorR.translate(x=0.2, y=-0.3, z=0.5)
    sensorR.rotate(z=-0.523)
    sensorR.properties(Visible_arc=False, resolution=1, scan_window=60,
                       laser_range=5)
    sensorR.create_sick_arc()
    devices.append(sensorR)

    for device in devices:
        robot.append(device)
        device.configure_mw('socket')

env = Environment('custom/base')
env.place_camera([0, 0, 30])
env.aim_camera([0, 0, 0])
