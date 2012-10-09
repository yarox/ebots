from morse.builder.morsebuilder import *


devices = []

robot = Robot('atrv')
robot.name = 'robot'
robot.translate(x=-6.0, y=0, z=0.2)

motion = Actuator('v_omega')
motion.name = 'motion'
devices.append(motion)

camera = Sensor('semantic_camera')
camera.name = 'cam'
camera.translate(x=0, y=0, z=0.9)
devices.append(camera)

control = Actuator('keyboard')
control.properties(Speed=3.0)
devices.append(control)

for device in devices:
    robot.append(device)
    device.configure_mw('socket')

env = Environment('custom/base')
env.place_camera([0, 0, 30])
env.aim_camera([0, 0, 0])
